# Functions to generate meaningless UV sensor data (sinusoids) and to
# convert that data to the expected format

from math import sin
from random import randrange
from common_library import twos_comp

AMP_DIFF = 100
STEP_SIZE = 0.1

UVA_AMP = randrange(8000+AMP_DIFF)
UVB_AMP = randrange(10000+AMP_DIFF)
UVC1_AMP = randrange(3200+AMP_DIFF)
UVC2_AMP = randrange(4700+AMP_DIFF)
UVD_AMP = randrange(2000+AMP_DIFF)


def sine_generator(step_size, amplitude):
    x = 0
    while True:
        yield amplitude + amplitude * sin(x)
        x += step_size
        
uva = sine_generator(STEP_SIZE, UVA_AMP)
uvb = sine_generator(STEP_SIZE, UVB_AMP)
uvc1 = sine_generator(STEP_SIZE, UVC1_AMP)
uvc2 = sine_generator(STEP_SIZE, UVC2_AMP)
uvd = sine_generator(STEP_SIZE, UVD_AMP)

def make_fake_uv():
    return next(uva), next(uvb), next(uvc1), next(uvc2), next(uvd)

def uv_conversion(uva, uvb, uvc1, uvc2, uvd):
    # CONSTANTS, for open-air systems with and without a teflon diffusor over the VEML6075

    output = [0] * 13

    # Flags
    high_dynamic = 0
    trigger = 1
    powered_on = 1

    # Set integration times for UVA, UVB, and UVD, in ms
    uv_int1 = 0
    uv_int2 = 0
    uv_int3 = 0

    # Scale UVA data to a 16-bit resolution

    # Set output bytes for UV data
    output[12] = uvc2
    output[11] = uvc1
    output[10] = uvb
    output[9] = uvd
    output[8] = uva

    # Set output bytes for flags and integration times
    output[6] = uv_int3
    output[5] = uv_int2
    output[4] = uv_int1
    output[3] = high_dynamic
    output[1] = trigger
    output[0] = powered_on

    return output
