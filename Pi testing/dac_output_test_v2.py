# Old DAC test -- not sure what the deal is here, but use the other one.

import busio
from board import *
from adafruit_bus_device.i2c_device import I2CDevice
import time
import math

register = 0x4 #channel 4 (thermistor)

#i2c = I2C(5,3)
#i2c = board.I2C()

with busio.I2C(SCL, SDA) as i2c:
    dac1 = I2CDevice(i2c, 0x28)
    i = 0
    while True:
        msg = math.floor(128 * (math.sin(i/100) + 1))
        with dac1:
            device.write([register, msg])
        i += 1
        time.sleep(0.01)