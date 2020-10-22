import datetime
now = datetime.datetime.now
from random import random

newdata = [round(random() * 1000, 4) for i in range(12)]

t1 = now()
with open("sample_data.csv", "w") as f:
    for val in newdata:
        f.write(str(val) + " ")
t2 = now()
print(t2.microsecond - t1.microsecond)