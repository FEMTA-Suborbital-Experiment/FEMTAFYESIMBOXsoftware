import busio
from datetime import datetime, timedelta
from time import sleep

# Set up I2C for ADC control
i2c = busio.I2C(3, 2) #SCL, SDA

# Function to wait for I2C lock to be given
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
        sleep(0.1)  # Don't hog the processor busywaiting
    print("\nI2C lock obtained")