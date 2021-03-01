# A nice little function to add random noise to the sensor data.

from random import gauss
from numba import jit, float64


@jit(float64)
def fuzz(value, factor=0.01):
    return gauss(value, factor * value)
