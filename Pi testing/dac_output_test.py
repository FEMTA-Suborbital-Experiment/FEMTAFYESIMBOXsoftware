import board
import busio
import time

import math #just for output sine


address = 0x28 #DAC #1
register = 0x4 #channel 4 (thermistor)

bus = smbus.SMBus(1)

i = 0
while True:
    #msg = math.floor(128 * (math.sin(i/100) + 1))
    bus.write_i2c_block_data(address, 0, [register, 128 * (i%2)])
    i += 1
    time.sleep(2)