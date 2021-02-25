# Collection of commonly-used functions across multiple modules.

import math
from numba import jit, uint16, int16


@jit(uint16(int16))
def twos_comp(num):
    return num if num >= 0 else 65536 + num


@jit(uint16)
def sine_generator(step_size, amplitude):
    x = 0
    while True:
        yield amplitude + amplitude * math.sin(x)
        x += step_size
