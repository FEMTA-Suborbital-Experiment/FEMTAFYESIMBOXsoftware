# Main file to run on Raspberry Pi to coordinate simbox operations.

from time import sleep
from datetime import datetime, timedelta
now = datetime.now
import multiprocessing as mp
import multiprocessing.shared_memory as sm
#import socket #for BO flight events over Ethernet, eventually

import numpy as np
from numba import jit
import serial
import busio
import RPi.GPIO as GPIO
from timeloop import Timeloop

from config_parser import configs
from flow_conversion import flow_to_bytes
from mass_spec import make_fake_ms
from uv_conversion import uv_conversion, make_fake_uv
from add_noise import fuzz
from condition_functions import poll_valve_states, get_flight_conditions
from Simulation.sim import run as run_sim
from serial_interface import ArduinoI2CSimInterface
from i2c_interface import i2c, waitForI2CBusLock # I2C set up in an import file

# Define Serial port info
ARDUINO_PORT = "/dev/ttyACM0"
SERIAL_BAUD = 115200

# Define addresses
DAC = (0x28, 0x29) #DAC I2C addresses
# DAC0: pressure sensors & thermistors 1-4
# DAC1: mass spec, IR flow & thermistor 5
P = (0x0, 0x1, 0x2, 0x3) #Pressure sensor DAC channels
T = (0x4, 0x5, 0x6, 0x7, 0x0) #Thermistor DAC channels
MS = (0x4, 0x5) #Mass spec DAC channels
IR = (0x6, 0x7) #IR flow sensor DAC channels


# Define GPIO pins
GPIO_PINS = (4, 14, 15, 17, 18, 27) #not set in stone
RED, GRN = 21, 13


# Define (inverse) calibrations (units -> voltage)
pres_cals = (lambda x: 0.2698*x + 0.1013, lambda x: 0.2462*x + 0.4404,
             lambda x: 0.2602*x + 0.1049, lambda x: 0)
therm_cals = (lambda x: 0, lambda x: 0,
              lambda x: 0, lambda x: 0,
              lambda x: 0)

# Set up Arduino
digital_sensor_interface = ArduinoI2CSimInterface(port=ARDUINO_PORT, baudrate=SERIAL_BAUD)

# Set up shared memory
sensor_mem = sm.SharedMemory(name="sensors", create=True, size=120) #Edit with correct size
sim_mem = sm.SharedMemory(name="simulation", create=True, size=4)
sensor_data = np.ndarray(shape=(15,), dtype=np.float64, buffer=sensor_mem.buf)
sim_data = np.ndarray(shape=(4,), dtype=np.float64, buffer=sim_mem.buf)

valve_states = np.ndarray(shape=(6,), dtype=np.bool)
valve_states[:] = [True, True, True, True, True, True] # Edit to appropriate starting states

# GPIO setup
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.IN)

# Miscellaneous setup and initialization
start_t = 0
tl = Timeloop()
times = configs["event_times"]
h = np.load("matlab-python testing/Test Simulation/altitude.npy").reshape((99840,))
t = np.load("matlab-python testing/Test Simulation/time.npy").reshape((99840,))
altitude = 0

"""
Note on sensor failures:
There are two types of failure: first, digital sensors can stop
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
@jit
def run():
    global sensor_data, valve_states, error_state, start_t, sim_data
    
    # Set start time
    if not start_t:
        GPIO.output(GRN, GPIO.HIGH)
        start_t = now()

    # Determine new sensor failures
    for period in configs["dig_error_states"]:
        if period[0] <= now() - start_t < period[1]:
            error_state = period[2]

    for period in configs["all_error_states"]:
        if period[0] <= now() - start_t < period[1]:
            sensor_failures = period[2]
    
    # Incoming sensor data: (15 floats)
    # pres0, pres1, pres2, pres3, therm0, therm1, therm2, therm3, therm4,
    # dig_flow0, dig_flow1, dig_temp0, dig_temp1, ir_flow0, ir_flow1
    
    # Process data (only read from 'sensor_data' (<- shared array); mutate 'sensors')
    sensors = [fuzz(d) for d in sensor_data[:13]] + list(sensor_data[13:]) #boolean IR doesn't need noise
    for i in range(9):
        #i + 3 below makes the two different sets of indices line up (15 data values, 16 sensors, in diffrent orders)
        if sensor_failures[i + 3] == 1: #min
            sensors[i] = 0
        elif sensor_failures[i + 3] == 2: #max
            sensors[i] = 255 #TODO: what is the max value in this context? 1? 255?
        else: #normal operation
            if i < 4: #pressure sensors
                sensors[i] = pres_cals[i](sensors[i])
            else: #thermistors
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
            sensors[i] = 1
    
    #Prepare digital data to send to Arduino
    #9 bytes for each flow, 10 for UV, 1 for error state
    f0_data = flow_to_bytes(sensors[8], sensors[10], sensor_failures[0])
    f1_data = flow_to_bytes(sensors[9], sensors[11], sensor_failures[1])
    #uv_data = uv_conversion(uva, uvb, uvc1, uvc2, uvd) -> removed uvd for now
    uv_data = uv_conversion(uva, uvb, uvc1, uvc2)
    digital_data = [error_state, *f0_data, *f1_data, *uv_data]
    
    #Prepare analog data to send to DACs
    analog_data_0 = [P[0], sensors[0], P[1], sensors[1],
                     P[2], sensors[2], P[3], sensors[3],
                     T[0], sensors[4], T[1], sensors[5],
                     T[2], sensors[6], T[3], sensors[7]]
    analog_data_1 = [MS[0], mass0, MS[1], mass1,
                     IR[0], sensors[12], IR[1], sensors[13], 
                     T[4], sensors[8]]
    
    #Output data
    i2c.writeto(DAC[0], analog_data_0)
    i2c.writeto(DAC[1], analog_data_1)
    digital_sensor_interface.sendCommand(digital_data)
    
    #Valve feedback
    valve_states[:] = [GPIO.input(pin) for pin in GPIO_PINS]


    # Set Conditions
    sim_cond, flowSol, ventSol = poll_valve_states(valve_states)
    flight_cond = get_flight_conditions(start_t, times)
    altitude = np.interp(now() - start_t, t, h)

    sim_data[0] = altitude
    sim_data[1] = flowSol
    sim_data[2] = ventSol
    sim_data[3] = (now() - start_t).total_seconds()
    
    
if __name__ == "__main__":
    try:
        waitForI2CBusLock(1.0)      # Wait for exclusive access to I2C port (usually instant)
        digital_sensor_interface.connect()

        venv = mp.Process(target=run_sim, kwargs={"main_freq": 1/(configs["freqency"])})
        digital_sensor_interface.start() # Start mp Process
        venv.start()
        tl.start(block=True)
        venv.join()
    finally:
        #Turn off LEDs
        GPIO.output(GRN, GPIO.LOW)
        GPIO.output(RED, GPIO.LOW)

        venv.close()

        #Close shared memory
        sensor_mem.close()
        sim_mem.close()
        sensor_mem.unlink()
        sim_mem.unlink()

        # Close up busses when done
        digital_sensor_interface.close()
        i2c.unlock()
        i2c.deinit()
