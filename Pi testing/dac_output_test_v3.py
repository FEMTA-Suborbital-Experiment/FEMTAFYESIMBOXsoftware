import busio
from board import SDA, SCL
import time
import math

DEVICE      = 0x28
REGISTER    = 0x4   #channel 4 (thermistor)

with busio.I2C(SCL, SDA) as i2c:
    try:
        while not i2c.try_lock():
            pass
        
        i = 0
        while True:
            val = math.floor(128 * (math.sin(i/100) + 1))
            msg = bytes([REGISTER, val])
            i2c.writeto(DEVICE, msg)
            print(f"Sent '{' '.join(f'{b:#04x}' for b in msg)}', i={i}", end='\r')
            i += 1
            time.sleep(0.01)

    finally:
        i2c.unlock()