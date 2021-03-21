# Function to wait for I2C lock to be given

import time
from datetime import datetime, timedelta

from main import DEBUG
from smbx_logging import Logger

if not DEBUG:
    # Set up I2C for ADC control
    import busio
    i2c = busio.I2C(3, 2) #SCL, SDA
else:
    class I2C():
        """Stand-in class for debugging I2C interface"""
        def __init__(self):
            self.log = Logger("I2C")
            self.log.start()

            self._have_lock = False
            self._lock_t = -1

        def try_lock(self):
            if self._lock_t == -1:
                self._lock_t = time.perf_counter()
            else:
                return time.perf_counter() - self._lock_t > 0.25

        def writeto(self, address, data):
            self.log.write(f"{data} -> {address}", "i2c_debug.txt")

        def unlock(self):
            pass

        def deinit(self):
            self.log.close()

    i2c = I2C()

"""
Obtaining I2C lock grants sole access to the I2C bus and it is good practice to request a
lock to ensure stability and predictability. The I2C bus can be run without obtaining a
lock without issues assuming nothing else will try to touch the bus.
"""
def waitForI2CBusLock(timeout=1.0):
    print("Waiting for lock on I2C bus to be granted", end='')
    t_start = datetime.now()
    t_delta = timedelta(seconds=timeout)
    while not i2c.try_lock():
        if datetime.now() - t_start > t_delta:
            raise RuntimeError("Waiting for I2C lock port timed out")
        print(".", end='')
        time.sleep(0.1)  # Don't hog the processor busywaiting
    print("\nI2C lock obtained")