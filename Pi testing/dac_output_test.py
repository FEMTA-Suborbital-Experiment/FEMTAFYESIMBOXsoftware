from busio import I2C
import time

import math #just for output sine

address = 0x28 #DAC #1
register = 0x4 #channel 4 (thermistor)

i2c = I2C(5,3)

i = 0
while True:
    msg = math.floor(128 * (math.sin(i/100) + 1))
    i2c.writeto(address, [register, msg])
    i += 1
    time.sleep(0.01)