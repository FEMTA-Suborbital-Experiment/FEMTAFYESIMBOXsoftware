import datetime
now = datetime.datetime.now

t1 = now()
with open("sample_data.csv", "r") as f:
    data = readline()
t2 = now()
print(t2.microsecond - t1.microsecond)