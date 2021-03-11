# Stand-in for sim.py to test how numba handles a shared memory array

import time
import multiprocessing.shared_memory as sm

import numpy as np
from numba import njit


@njit(cache=False) #doesn't work when cache=True -> why?
def sim(ary):
    i = 0

    while True:
        i += 1
        if not i % 10:
            print("sim i:", i, "ary:", ary[0])
            yield


def run():
    try:
        test_mem = sm.SharedMemory(name="test")
        test_ary = np.ndarray(shape=(1,), dtype=np.float64, buffer=test_mem.buf)

        sim_gen = sim(test_ary)

        while True:
            start_next = time.time() + 1
            for _ in range(10):
                next(sim_gen)
            
            duration = start_next - time.time()
            if duration > 0:
                time.sleep(duration)
        
    except:
        test_mem.close()
