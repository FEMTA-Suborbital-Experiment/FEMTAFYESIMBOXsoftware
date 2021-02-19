# Simple function to make sine-wave mass-spec data

from common_library import sine_generator

STEP_SIZE = 0.1
AMP0 = 50
AMP1 = 60

mass0_gen = sine_generator(STEP_SIZE, AMP0)
mass1_gen = sine_generator(STEP_SIZE, AMP1)

def make_fake_ms(state0, state1):
    vals = next(mass0_gen), next(mass1_gen)

    if state0 == 0: #normal
        mass0 = vals[0]
    elif state0 == 1: #min
        mass0 = 0
    elif state0 == 2: #max
        mass0 = AMP0

    if state1 == 0: #normal
        mass1 = vals[1]
    elif state1 == 1: #min
        mass1 = 0
    elif state0 == 2: #max
        mass1 = AMP1

    return mass0, mass1
