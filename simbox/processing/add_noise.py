# A nice little function to add random noise to the sensor data.

from random import gauss

def fuzz(value, factor=0.01):
    return gauss(value, factor * value)
