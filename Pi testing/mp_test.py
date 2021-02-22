# General-purpose multiprocessing test sandbox

import multiprocessing as mp
import time

def f():
    time.sleep(1)

def test():
    p = mp.Process(target=f, args=())
    t = time.time()
    p.start()
    print(time.time() - t)
    p.join()
    print(time.time() - t)

if __name__ == "__main__":
    test()