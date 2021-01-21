# Main file to run on Raspberry Pi to coordinate simbox operations.
# The Pi should eventually be configured to run this program on boot,
# with the only other program running on boot being the Matlab simulation.

from timeloop import Timeloop
from datetime import datetime, timedelta
import serial           #USB
from busio import I2C   #I2C
import board            #I2C
#import socket           #Ethernet and Matlab
import RPi.GPIO as GPIO #GPIO (valve feedback & LEDs)

from flow_conversion import flow_to_bytes
from mass_spec import make_fake_ms
from uv_conversion import uv_conversion, make_fake_uv
from add_noise import fuzz


FREQUENCY = 20 #Hz
ERROR_STATE = 0 #Default is to keep this constant


#Define addresses
DAC = (0x28, 0x29) #DAC I2C addresses
#DAC0: pressure sensors & thermistors; DAC1: mass spec & IR flow
P = (0x0, 0x1, 0x2, 0x3) #Pressure sensor DAC channels
T = (0x4, 0x5, 0x6, 0x7) #Thermistor DAC channels
MS = (0x0, 0x1) #Mass spec DAC channels
IR = (0x2, 0x3) #IR flow sensor DAC channels


#Define GPIO pins
GPIO_PINS = (4, 14, 15, 17, 18, 27) #not set in stone
RED, GRN = 21, 13


# Define (inverse) calibrations (units (which?) -> voltage)
pres_cals = (lambda x: 0.2698*x + 0.1013, lambda x: 0.2462*x + 0.4404,
             lambda x: 0.2602*x + 0.1049, lambda x: 0)
therm_cals = (lambda x: 0, lambda x: 0,
              lambda x: 0, lambda x: 0)


#Set up connections (and misc.)
start_t = 0
tl = Timeloop()
i2c = board.I2C()
arduino = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
arduino.flush()
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
for pin in GPIO_PINS:
    GPIO.setup(pin, GPIO.IN)


@tl.job(interval=timedelta(seconds=1/FREQUENCY))
def run():
    #Set start time
    if not start_t:
        GPIO.output(GRN, GPIO.HIGH)
        start_t = datetime.datetime.now()
    
    #Receive sensor data from Matlab
    sensor_data = list(matlab.read())
    #pres0, pres1, pres2, pres3, therm0, therm1, therm2, therm3,
    #dig_flow0, dig_flow1, dig_temp0, dig_temp1, ir_flow0, ir_flow1
    
    #Process data
    sensor_data = [fuzz(d) for d in sensor_data]
    for i in range(4):
        sensor_data[i] = pres_cals[i](sensor_data[i])
        sensor_data[i+4] = therm_cals[i](sensor_data[i+4])
        
    #Make fake UV and mass spec. data
    uva, uvb, uvc1, uvc2, uvd = make_fake_uv()
    mass0, mass1 = make_fake_ms()
    
    #Prepare digital data to send to Arduino
    #9 bytes for each flow, 10 for UV, 1 for error state
    f0_data = flow_conversion(sensor_data[8], sensor_data[10])
    f1_data = flow_conversion(sensor_data[9], sensor_data[11])
    uv_data = uv_conversion(uva, uvb, uvc1, uvc2, uvd)
    digital_data = [*f0_data, *f1_data, *uv_data, ERROR_STATE]
    
    #Prepare analog data to send to DACs
    analog_data_0 = [P[0], sensor_data[0], P[1], sensor_data[1],
                     P[2], sensor_data[2], P[3], sensor_data[3],
                     T[0], sensor_data[4], T[1], sensor_data[5],
                     T[2], sensor_data[6], T[3], sensor_data[7]]
    analog_data_1 = [MS[0], mass0, MS[1], mass1,
                     IR[0], sensor_data[12], IR[1], sensor_data[13]]
    
    #Output data
    i2c.writeto(DAC[0], analog_data_0)
    i2c.writeto(DAC[1], analog_data_1)
    arduino.write(bytes(digital_data))
    
    #Valve feedback
    valves = [GPIO.input(pin) for pin in GPIO_PINS]
    matlab.write(valves)
    
    
if __name__=='__main__':
    try:
        tl.start(block=True)
    finally:
        #Clean up by turning off LEDs
        GPIO.output(GRN, GPIO.LOW)
        GPIO.output(RED, GPIO.LOW)