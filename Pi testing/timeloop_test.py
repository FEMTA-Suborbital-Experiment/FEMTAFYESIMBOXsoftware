# Test the functionality of the Timeloop module
# 
# It allows a function to be run on a loop, executing every X seconds,
# taking into account the time it takes the function itself to run.
# 
# It seems that the module is a bit broken right off of PyPI, but I've modified
# the source on the Pi's version of it to fix it, and it now works as expected.

from datetime import datetime, timedelta
now = datetime.now
from timeloop import Timeloop
from math import sqrt

def raw_times():
    for i in range(10):
        t0 = now()
        [sqrt(i) for i in range(1000000)]
        t1 = now()
        print(t1 - t0)
   
   
tl = Timeloop()
prev = now()

@tl.job(interval=timedelta(seconds=2))
def test_func():
    global prev
    print(now() - prev)
    prev = now()
    [sqrt(i) for i in range(1000000)]
    
def tloop():
    tl.start(block=True)
    
if __name__=='__main__':
    from time import sleep
    raw_times()
    sleep(1)
    tloop()