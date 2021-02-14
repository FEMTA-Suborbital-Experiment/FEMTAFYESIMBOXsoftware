# This functionality is not needed; see mp_shared_mem.py

# Test for a simple inter-process buffer that might be used to communicate between 
# the virtual environment sim and the main simbox program. Uses a lock to ensure
# reading and writing don't conflict. The test below creates two process that 
# try to use the same buffer at the same time (every 10 sec). The test doesn't work.

from types import BuiltinFunctionType

class Buffer:
    """Simple one value buffer that prevents concurrency conflicts"""
    def __init__(self, lock):
        self.value = None
        if isinstance(lock, BuiltinFunctionType):
            self._lock = lock()
        else:
            self._lock = lock
    
    def put(self, value):
        with self._lock:
            self.value = value

    def get(self):
        with self._lock:
            return self.value


if __name__ == "__main__":
    import threading as th
    import multiprocessing as mp 
    import time
    from math import floor

    def f(buff, method):
        i = 0
        while i <= 100:
            if not floor(time.time()) % 10:
                if method == "put":
                    buff.put(i)
                else:
                    print(buff.get(i))
                i += 1
            time.sleep(1)
        
    buff = Buffer(th.Lock())
    putter = mp.Process(target=f, args=(buff, "put"))
    getter = mp.Process(target=f, args=(buff, "get"))
    putter.start()
    getter.start()
