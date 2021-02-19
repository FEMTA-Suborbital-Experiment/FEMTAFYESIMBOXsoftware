# The following functions determine simulation and flight conditions.
# The former checks the valve states and sets a simulation condition
# based on the states of the flow solenoid and the vent solenoids.
# The latter determines the time passed and sets a flight condition
# based on whether the time passed is greater than the preset
# elements of the flight condition.
from datetime import datetime

now = datetime.now


# valve_states is a boolean six-element list
# if none of the valve states are open or
# the flow solenoid is open (undefined), return 0 (false)
def poll_valve_states(valve_states):
    sim_condition = 0

    if valve_states[0] and valve_states[1] and valve_states[2]:
        sim_condition = 3
    elif valve_states[0] and valve_states[1]:
        sim_condition = 1
    elif (valve_states[1] and valve_states[2]) or (valve_states[0] and valve_states[2]):
        sim_condition = 4
    elif valve_states[0] or valve_states[1]:
        sim_condition = 2
    return sim_condition


# time is a datetime object that represents the past
# times is a 5-tuple that represent the critical points of the simulation
def get_flight_condition(time, times):

    flight_condition = 0

    time_passed = (now() - time).total_seconds()

    if time_passed >= times[3]:
        flight_condition = 3
    elif time_passed >= times[1]:
        flight_condition = 2
    else:
        flight_condition = 1
    return flight_condition
