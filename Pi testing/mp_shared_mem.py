# Test of how the virtual environment process might pass data to and from
# the simbox parent process. **Don't run this file as-is**; run it in two 
# separate Python processes (simplest: two shells), entering code in each
# process in order, going down the page.
# This seems to work great!


# -=-=- Process 1 -=-=-

import numpy as np
import multiprocessing.shared_memory as sm

# Set up and initialize shared array
# Note: mem size and array shape and dtype should be determined for our 
# specific purposes. Here it's an array of 6 bools (1 byte each)
mem = sm.SharedMemory(create=True, name="valve_states", size=6)
valves = np.ndarray((6,), dtype=np.bool, buffer=mem.buf)
valves[:] = [False, False, True, False, False, True]
# valves is now useable as an array in Process 1. 

# -=-=- Process 2 -=-=-

import numpy as np
import multiprocessing.shared_memory as sm

# Create array using the same shared memory
# Note that the shape and dtype shoudl eb the same as defined above
mem = sm.SharedMemory(name="valve_states")
valves = np.ndarray((6,), dtype=np.bool, buffer=mem.buf)
# valves is now useable as an array in Process 2. It shares the same data
# as the array in Process 1

print(valves)
valves[:] = [True, True, True, False, False, False]

# -=-=- Process 1 -=-=-
print(valves) #should be modified

mem.close()

# -=-=- Process 2 -=-=-
mem.close()
mem.unlink() #call close() once per process; call unlink() once overall