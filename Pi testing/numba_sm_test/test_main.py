# Stand-in for main.py to test how numba handles a shared memory array

from datetime import timedelta
import multiprocessing as mp
import multiprocessing.shared_memory as sm

import numpy as np
from timeloop import Timeloop

from test_sim import run


test_mem = sm.SharedMemory(name="test", create=True, size=8)
test_ary = np.ndarray(shape=(1,), dtype=np.float64, buffer=test_mem.buf)
tl = Timeloop()

i = 0.0
test_ary[:] = i

@tl.job(interval=timedelta(seconds=1))
def loop():
    global i
    i += 1
    print("new i:", i)
    test_ary[:] = float(i)


try:
    sim = mp.Process(target=run)
    sim.start()
    tl.start(block=True)
    sim.join()

finally:
    if sim.is_alive():
        sim.terminate()
    sim.close()

    test_mem.close()
    test_mem.unlink()