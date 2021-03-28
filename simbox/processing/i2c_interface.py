# Function to wait for I2C lock to be given

import sys
import time

from .smbx_logging import Logger


DEBUG = "debug" in sys.argv


if DEBUG:
    class I2C():
        """Stand-in class for debugging I2C interface"""
        
        log = Logger("debug")
        log.start()

        def __init__(self):
            self._have_lock = False
            self._lock_t = -1

        def try_lock(self):
            if self._lock_t == -1:
                self._lock_t = time.perf_counter()
            else:
                self._have_lock = time.perf_counter() - self._lock_t > 0.25
                return self._have_lock

        def writeto(self, address, data):
            self.log.write(f"I2C {data} to {address:#x}", "i2c_debug.txt")

        def unlock(self):
            pass

        def deinit(self):
            self.log.close()

    i2c = I2C()

else:
    # Set up I2C for ADC control
    import busio
    i2c = busio.I2C(3, 2) #SCL, SDA


"""
Obtaining I2C lock grants sole access to the I2C bus and it is good practice to request a
lock to ensure stability and predictability. The I2C bus can be run without obtaining a
lock without issues assuming nothing else will try to touch the bus.
"""
def waitForI2CBusLock(timeout=1.0):
    log = Logger("I2C")
    log.start()

    log.write("Waiting for lock on I2C bus to be granted", "low_freq.txt", True, end="")
    t_start = time.time()
    while not i2c.try_lock():
        if time.time() - t_start > timeout:
            raise RuntimeError("Waiting for I2C lock timed out")
        print(".", end='')
        time.sleep(0.1)  # Don't hog the processor busywaiting
    print()
    log.write("I2C lock obtained", "low_freq.txt", True)

    log.close()
