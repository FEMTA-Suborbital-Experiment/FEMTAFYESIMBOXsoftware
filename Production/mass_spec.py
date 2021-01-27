from common_library import sine_generator

STEP_SIZE = 0.1
AMP1 = 50
AMP2 = 60

mass0 = sine_generator(STEP_SIZE, AMP1)
mass1 = sine_generator(STEP_SIZE, AMP2)


def make_fake_ms():
    return next(mass0), next(mass1)
