# Main file to run on Raspberry Pi to coordinate simbox operations.

# Check for debug mode
import sys
DEBUG = "debug" in sys.argv

# Imports
import time
from datetime import timedelta
import multiprocessing as mp
import multiprocessing.shared_memory as sm
#import socket #for BO flight events over Ethernet, eventually

import numpy as np
from timeloop import Timeloop

if DEBUG:
    from .processing.debug_gpio import GPIO
else:
    import RPi.GPIO as GPIO

from .processing.config_parser import configs
from .processing.flow_conversion import flow_to_bytes
from .processing.mass_spec import make_fake_ms
from .processing.uv_conversion import uv_conversion, make_fake_uv
from .processing.add_noise import fuzz
from .processing.condition_functions import poll_valve_states #, get_flight_conditions
from .processing.serial_interface import ArduinoI2CSimInterface
from .processing.i2c_interface import i2c, waitForI2CBusLock # I2C set up in an import file
from .processing.smbx_logging import Logger
from .processing.common_library import byte
from .simulation.sim import run as run_sim


# Define Serial port info
ARDUINO_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 115200


# Define addresses
DAC = (0x28, 0x29) #DAC I2C addresses
# DAC0: pressure sensors & thermistor 5
# DAC1: mass spec, IR flow & thermistors 1-4
P = (0x4, 0x5, 0x6, 0x7) #Pressure sensor DAC channels
T = (0x0, 0x1, 0x2, 0x3, 0x0) #Thermistor DAC channels
MS = (0x4, 0x5) #Mass spec DAC channels
IR = (0x6, 0x7) #IR flow sensor DAC channels


# Define GPIO pins
GPIO_PINS = (23, 24, 10, 9, 8, 7) #flow sol 1 open, flow sol 1 close, flow2, vent
RED, GRN = 21, 13


# Define (inverse) calibrations (units -> voltage)
pres_cals = (lambda x: 0.2698*x + 0.1013, lambda x: 0.2462*x + 0.4404,
             lambda x: 0.2602*x + 0.1049, lambda x: 0)
therm_cals = (lambda x: 0, lambda x: 0,
              lambda x: 0, lambda x: 0,
              lambda x: 0) #TODO: enter final calibrations


# Set up Arduino
digital_sensor_interface = ArduinoI2CSimInterface(port=ARDUINO_PORT, baudrate=SERIAL_BAUD, debug=DEBUG)


# Set up shared memory
sensor_mem = sm.SharedMemory(name="sensors", create=True, size=1200)
sim_mem = sm.SharedMemory(name="simulation", create=True, size=32)
sensor_data = np.ndarray(shape=(10, 15), dtype=np.float64, buffer=sensor_mem.buf)
sim_data = np.ndarray(shape=(4,), dtype=np.float64, buffer=sim_mem.buf)


# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.IN)


# Miscellaneous setup and initialization
tl = Timeloop()
log = Logger("main")
start_t = 0
times = configs["event_times"]
h = np.load("simbox/simulation/altitude.npy")
t = np.load("simbox/simulation/time.npy")
altitude = 0
sensor_data_index = -1 #since the increment is done before the read, and we want to start at 0
valve_states = [0, 0, 1] #flow 1, flow 2, vent. 0 = closed, 1 = open


"""
Note on sensor failures:
There are two types of failures: first, digital sensors can stop
responding over I2C. This data comes from the config parser in
config["dig_error_states"], and is stored here for each loop in error_state.
The other type can apply to any sensor, and it is setting it at maximum
or minimum output. This comes from config["all_error_states"] and
is saved here in sensor_failures.
"""
error_state = 0 #Making I2C sensors stop responding
sensor_failures = [0] * 16 #All sensors, normal/min/max. Indices:
# Flow0, Flow1, UV, Pres0, Pres1, Pres2, Pres3, Therm0, 
# Therm1, Therm2, Therm3, Therm4, Mass0, Mass1, IR0, IR1


#Main looping function
@tl.job(interval=timedelta(seconds=1/(configs["frequency"])))
def run():
    global sensor_data, sensor_data_index, error_state, start_t, sim_data, error_state, sensor_failures #not really needed, but ok to have
    
    # To be run on first loop
    if not start_t:
        GPIO.output(GRN, GPIO.HIGH)
        start_t = time.time()

    # Determine new sensor failures
    for period in configs["dig_error_states"]:
        if period[0] <= time.time() - start_t < period[1]:
            if period[2] != error_state:
                log.write(f"New digital error state {period[2]}", "low_freq.txt", True)
            error_state = period[2]

    for period in configs["all_error_states"]:
        if period[0] <= time.time() - start_t < period[1]:
            if period[2] != sensor_failures:
                changes = list()
                for i in range(16):
                    if period[2][i] != sensor_failures[i]:
                        changes.append(f"index {i} changed from {sensor_failures[i]} to {period[2][i]}")
                log.write(f"Change{'s' if len(changes) != 1 else ''} in general error state: {'; '.join(changes)}", "low_freq.txt", True)
            sensor_failures = period[2]

    
    # Process data (only read from 'sensor_data' (<- shared array); mutate 'sensors')
    # Use appropriate row of array, going from 0 to 9 repeatedly
    sensor_data_index = (sensor_data_index + 1) % 10
    sensors = [fuzz(d) for d in sensor_data[sensor_data_index]]

    # Incoming sensor data: (15 floats)
    # pres0, pres1, pres2, pres3, therm0, therm1, therm2, therm3, therm4,
    # dig_flow0, dig_flow1, dig_temp0, dig_temp1, ir_flow0, ir_flow1

    # Handle sensor failures for pressure and temperature sensors; apply sensor calibration curves if not in an error state
    for i in range(9):
        # i + 3 below makes the two different sets of indices line up (15 data values, 16 sensors, in diffrent orders)
        if sensor_failures[i + 3] == 1: # min
            sensors[i] = 0
        elif sensor_failures[i + 3] == 2: # max
            sensors[i] = 255
        else: # normal operation
            if i < 4: # pressure sensors
                sensors[i] = pres_cals[i](sensors[i])
            else: # thermistors
                sensors[i] = therm_cals[i - 4](sensors[i])
        
    # Make fake UV and mass spec. data 
    #uva, uvb, uvc1, uvc2, uvd = make_fake_uv(sensor_failures[2]) -> removed uvd for now
    uva, uvb, uvc1, uvc2 = make_fake_uv(sensor_failures[2])
    mass0, mass1 = make_fake_ms(sensor_failures[12], sensor_failures[13])

    # Process IR error states
    for i in (13, 14):
        if sensor_failures[i + 1] == 1: #min
            sensors[i] = 0
        elif sensor_failures[i + 1] == 2: #max
            sensors[i] = 255
    
    # Prepare digital data to send to Arduino
    # 9 bytes for each flow, 8 for UV, 1 for error state
    f0_data = flow_to_bytes(sensors[8], sensors[10], sensor_failures[0])
    f1_data = flow_to_bytes(sensors[9], sensors[11], sensor_failures[1])
    #uv_data = uv_conversion(uva, uvb, uvc1, uvc2, uvd) -> removed uvd for now
    uv_data = uv_conversion(uva, uvb, uvc1, uvc2)
    digital_data = [error_state, *f0_data, *f1_data, *uv_data]
    
    # Prepare analog data to send to DACs
    for i in range(9):
        sensors[i] = byte(sensors[i])
    mass0 = byte(mass0)
    mass1 = byte(mass1)
    sensors[12] = byte(sensors[12])
    sensors[13] = byte(sensors[13])

    analog_data_0 = [P[0], sensors[0], P[1], sensors[1],
                     P[2], sensors[2], P[3], sensors[3],
                     T[4], sensors[8]]
    analog_data_1 = [T[0], sensors[4], T[1], sensors[5],
                     T[2], sensors[6], T[3], sensors[7],
                     MS[0], mass0, MS[1], mass1,
                     IR[0], sensors[12], IR[1], sensors[13]]
    
    # Output data
    i2c.writeto(DAC[0], analog_data_0)
    i2c.writeto(DAC[1], analog_data_1)
    digital_sensor_interface.sendCommand(digital_data)
    
    # Valve feedback
    for index, name in [(0, "Flow Solenoid 1"), (1, "Flow Solenoid 2"), (2, "Vent Solenoid")]:
        if not GPIO.input(GPIO_PINS[2 * index]): #open; inverted logic
            log.write(f"Open commanded for {name}", "low_freq.txt", True)
            valve_states[index] = 1
        if not GPIO.input(GPIO_PINS[2 * index + 1]): #close; inverted logic
            log.write(f"Close commanded for {name}", "low_freq.txt", True)
            valve_states[index] = 0

    # Set Conditions
    flowSol, ventSol = poll_valve_states(valve_states) #sim_cond
    # flight_cond = get_flight_condition(now(), times)
    altitude = np.interp(time.time() - start_t, t, h)

    sim_data[0] = altitude
    sim_data[1] = flowSol
    sim_data[2] = ventSol
    sim_data[3] = time.time() - start_t

    # Log high-frequency data (93 values, mostly doubles (need to convert to str and join w/ commas))
    # lengths:   15        15       27            16             10             6             4
    # sensor_data[indx], sensors, digital_data, analog_data_0, analog_data_1, valve_states, sim_data
    # For now, let's write 6 decimals for floats e.g '3.141593' (may vary a bit w/ sci notation)
    to_log = [*sensor_data[sensor_data_index], *sensors, *digital_data, *analog_data_0, *analog_data_1, *valve_states, *sim_data]
    to_log = ",".join(map(lambda num: f"{num:.6g}", to_log))
    log.write(to_log, "main_hf.csv", False)
    
    
if __name__ == "__main__":
    try:
        waitForI2CBusLock(1.0)      # Wait for exclusive access to I2C port (usually instant)
        digital_sensor_interface.connect()

        venv = mp.Process(target=run_sim, kwargs={"dt": configs["dt"], "main_freq": configs["frequency"], "sensitivity": configs["sensitivity"]})
        digital_sensor_interface.start() # Start mp Process
        venv.start()
        log.start()
        tl.start(block=True)
        venv.join()

    finally:
        #End timeloop
        tl.stop()

        #Turn off LEDs
        GPIO.output(GRN, GPIO.LOW)
        GPIO.output(RED, GPIO.LOW)

        #Close child process
        if venv.is_alive():
            venv.terminate()
        venv.close()

        #Close logger
        log.close()

        #Close shared memory
        sensor_mem.close()
        sim_mem.close()
        sensor_mem.unlink()
        sim_mem.unlink()

        # Close up busses when done
        digital_sensor_interface.close()
        i2c.unlock()
        i2c.deinit()
