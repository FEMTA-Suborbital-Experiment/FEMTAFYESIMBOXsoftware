import smbus
import math #just for output sine

address = 0x28 #DAC #1
register = 0x4 #channel 4 (thermistor)

bus = smbus.SMBus(1)

i = 0
while True:
    msg = round(128 * (math.sin(i/10) + 1))
    bus.write_i2c_block_data(address, register, msg)
    i += 1