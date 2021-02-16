# Parser for config.txt. This will return 'machine-readable' configurations
# to the main script from a human-readable file.

class ConfigurationError(Exception):
    """Errors raised when parsing config file"""
    def __init__(self, message):
        self.message = message

try:
    with open("Production/config.txt", "r") as cfg: #maybe need to modify path here for the pi?
        src = cfg.read().split("::")[2::2]
except FileNotFoundError:
    raise ConfigurationError("The configuration file was not found")

configs = dict() #To be filled and outputted


# -=-=- Parse simbox frequency -=-=-
try:
    configs["freqency"] = int(src[0].strip().split()[0])
except TypeError:
    raise ConfigurationError("'Simbox Frequency' is missing or formatted incorrectly")


# -=-=- Parse event timing -=-=-
events = ["Launch", "Start of 0g", "Apogee", "End of 0g", "Landing"]
lines = src[1].strip().split("\n")

times = list()
for i in range(5):
    line = lines[i].split(";")
    if line[0] != events[i]:
        raise ConfigurationError(f"Event name for flight event #{i + 1} has been modified")

    try:
        times.append(float(line[-1].strip()))
    except TypeError:
        raise ConfigurationError(f"Non-numeric event time for event {line[0]}")

if times[0] != 0:
    raise ConfigurationError("Launch must occur at T+0")
elif len(times) != len(events):
    raise ConfigurationError("Flight event list has been modified")

flight_duration = times[4] - times[0]
configs["event_times"] = tuple(times)


# -=-=- Parse sensor failures -=-=-
sensors = ["flow0", "flow1", "uv", "pres0", "pres1", "pres2", "pres3", "therm0",
"therm1", "therm2", "therm3", "therm4", "mass0", "mass1", "ir0", "ir1"]
states = ["normal", "min", "max", "dead"]

# First, get a list of tuples of the form (name, state, time), where name and state are numeric
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
            failures[i][1] = states.index(failures[i][1].lower())
        except ValueError:
            raise ConfigurationError("Invalid sensor failure state")
    elif failures[i][1].isnumeric() and int(failures[i][1]) in range(4):
        failures[i][1] = int(failures[i][1])
    else:
        raise ConfigurationError("Invalid sensor failure configuration")

    if failures[i][1] == 3 and failures[i][0] > 2:
        raise ConfigurationError(f"Only digital sensors can fail to state Dead (line {i + 1})")

    try:
        failures[i][2] = float(failures[i][2])
    except ValueError:
        raise ConfigurationError(f"Invalid time for sensor failure #{i + 1}")
    
    if failures[i][2] < 0:
        raise ConfigurationError(f"Invalid time for sensor failure #{i + 1} (before liftoff)")
    if failures[i][2] > flight_duration:
        raise ConfigurationError(f"Invalid time for sensor failure #{i + 1} (after landing)")

failures.sort(key=lambda x: x[2])

# Next, convert digital sensor 'dead' failures to error states
dead_failures = [failure for failure in failures if (failure[0] < 3) and (failure[1] in (0, 3))]
error_states = [[0, flight_duration, 0]] #-> start_t, end_t, event state
for fail in dead_failures:
    sensor = 2 ** fail[0]
    state = bool(fail[1]) # i.e 1 if Dead, 0 if Normal
    time = fail[2]

    indx = -1
    for i in range(len(error_states)):
        if (error_states[i][0] < time) and (error_states[i][1] == flight_duration or error_states[i+1][0] > time):
            # insert a new tuple starting at transition time and taking the previous tuple's end time
            error_states.insert(i + 1, [time, error_states[i][1], error_states[i][2]])
            # set previous tuple's end time to transition time
            error_states[i][1] = time 
            indx = i
            break
        elif error_states[i + 1][0] == time:
            # no need for a new tuple
            indx = i
            break

    # bitwise xor with new state for each tuple, starting from the new one,
    # but only if there is a toggle to be done
    if (error_states[indx][2] & sensor) != state:
        for i in range(indx + 1, len(error_states)):
            error_states[i][2] ^= sensor

configs["dig_error_states"] = error_states

# Next, parse normal/min/max for all sensors 
# outputted: list of (start_t, end_t, <state>) like above but <state> is a 
# 16-list with each spot corresponding to a sensor and equal to either 
# 0, 1, or 2 (being Normal, Min, and Max)

all_failures = [f for f in failures if f[1] != 3]
error_states = [[0, flight_duration, [0]*16]] #-> start_t, end_t, state

for fail in all_failures:
    sensor = fail[0]
    state = fail[1]
    time = fail[2]

    indx = -1
    for i in range(len(error_states)):
        if (error_states[i][0] < time) and (error_states[i][1] == flight_duration or error_states[i+1][0] > time):
            # insert a new tuple starting at transition time and taking the previous tuple's end time
            error_states.insert(i + 1, [time, error_states[i][1], error_states[i][2].copy()])
            # set previous tuple's end time to transition time
            error_states[i][1] = time 
            indx = i
            break
        elif error_states[i + 1][0] == time:
            # no need for a new tuple
            indx = i
            break

    # update all following tuples with new state info
    for i in range(indx + 1, len(error_states)):
        error_states[i][2][sensor] = state

configs["all_error_states"] = error_states


if __name__ == "__main__":
    print(configs)
