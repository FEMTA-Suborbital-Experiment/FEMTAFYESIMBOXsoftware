# Parser for config.txt. This will return 'machine-readable' configurations
# to the main script from a human-readable file.

class ConfigurationError(SyntaxError):
    """Errors raised when parsing config file"""
    def __init__(self, message):
        self.message = message

with open("config.txt", "r") as c:
    src = c.read().split("::")[1::2]

configs = dict() #To be filled and outputted


#Parse simbox frequency
try:
    configs["freq"] = int(src[0].strip().split()[0])
except TypeError:
    raise ConfigurationError("'Simbox Frequency' is missing or formatted incorectly")


#Parse event timing
events = ["Launch", "Start of 0g", "Apogee", "End of 0g", "Landing"]
lines = src[1].strip().split("\n")

times = list()
for i in range(5):
    line = lines[i].split()
    if line[0] != events[i]:
        raise ConfigurationError(f"Event name for flight event \#{i + 1} has been modified")

    try:
        times.append(float(line[-1]))
    except TypeError:
        raise ConfigurationError(f"Non-numeric event time for event {line[0]}")

if times[0] != 0:
    raise ConfigurationError("Launch must occur at T+0")
elif len(times) != len(events):
    raise ConfigurationError("Flight event list has been modified")

configs["event_times"] = tuple(times)


#Parse sensor failures
sensors = ["flow0", "flow1", "uv", "pres0", "pres1", "pres2", "pres3", "therm0",
"therm1", "therm2", "therm3", "therm4", "mass0", "mass1", "ir0", "ir1"]
states = ["normal", "dead", "min", "max"]

#First, get a list of tuples of the form (name, state, time), where name and state are numeric
failures = src[2].strip().split("\n")
failures = [[i.strip() for i in line.split(";")][:3] for line in failures]

for i in range(len(failures)):
    if failures[i][0].lower() in sensors:
        try:
            failures[i][0] = sensors.index(failures[i][0].lower())
        except ValueError:
            raise ConfigurationError("Invalid sensor name")
    elif failures[i][0].isnumeric() and int(failures[i][0]) in range(16):
        failures[i][0] = int(failures[i][0])
    else:
        raise ConfigurationError("Invalid sensor failure configuration")

    if failures[i][1].lower() in states:
        try:
            failures[i][1] = sensors.index(failures[i][1].lower())
        except ValueError:
            raise ConfigurationError("Invalid sensor failure state")
    elif failures[i][1].isnumeric() and int(failures[i][1]) in range(4):
        failures[i][1] = int(failures[i][1])
    else:
        raise ConfigurationError("Invalid sensor failure configuration")

    if failures[i][1] == 1 and failures[i][0] > 2:
        raise ConfigurationError("Only digital sensors can fail to state Dead")

    try:
        failures[i][2] = float(failures[i][2])
    except ValueError:
        raise ConfigurationError(f"Invalid time for sensor failure \#{i + 1}")
    if failures[i][2] < 0:
        raise ConfigurationError(f"Invalid time for sensor failure \#{i + 1}")

#Next, convert digital sensors to error states

