# Quick test to see how quickly Python can read from a file. This would be
# important if we had gone with the quick-and-dirty interprocess communication
# of reading and writing to a shared file, but since we've moved to sockets, this
# isn't important anymore.

import datetime
now = datetime.datetime.now

t1 = now()
with open("sample_data.csv", "r") as f:
    data = f.readline()
t2 = now()
print(t2.microsecond - t1.microsecond)