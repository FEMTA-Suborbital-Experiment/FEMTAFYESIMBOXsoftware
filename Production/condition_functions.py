# The following functions determine simulation and flight conditions.
# The former checks the valve states and sets a simulation condition
# based on the states of the flow solenoid and the vent solenoids.
# The latter determines the time passed and sets a flight condition
# based on whether the time passed is greater than the preset
# elements of the flight condition.

#from datetime import datetime
#now = datetime.now


# Sim conditions not used throughout program
# valve_states is a boolean six-element list
# flow_solenoid is an integer representing number of flow solenoids open
# vent solenoid is a boolean representing an open (1) or closed (0) vent solenoid
def poll_valve_states(valve_states):
    # sim_condition = 0

    flow_solenoid = valve_states[0] + valve_states[1]
    vent_solenoid = valve_states[2]

    # if flow_solenoid > 1 and vent_solenoid:
    #    sim_condition = 3
    # elif flow_solenoid and vent_solenoid:
    #    sim_condition = 4
    # elif flow_solenoid > 1:
    #    sim_condition = 1
    # elif flow_solenoid:
    #    sim_condition = 2
    return flow_solenoid, vent_solenoid  # sim_condition,


# Flight condition not used throughout program
# time is a datetime object that represents the past
# times is a 5-tuple that represent the critical points of the simulation
# return a uint8-type flight condition
#def get_flight_condition(time, times):

#    flight_condition = 0

#    time_passed = (now() - time).total_seconds()

#    if time_passed >= times[3]:
#        flight_condition = 3
#    elif time_passed >= times[1]:
#        flight_condition = 2
#    else:
#        flight_condition = 1
#    return flight_condition
