# Functions to generate meaningless UV sensor data (sinusoids) and to
# convert that data to the expected format

from math import sin
from random import randrange
from common_library import twos_comp

STEP_SIZE = 0.1
AMP_DIFF = 200


UVA_AMP = randrange(8000-AMP_DIFF, 8000+AMP_DIFF)
UVB_AMP = randrange(10000-AMP_DIFF, 10000+AMP_DIFF)
UVC1_AMP = randrange(3200-AMP_DIFF, 3200+AMP_DIFF)
UVC2_AMP = randrange(4700-AMP_DIFF, 4700+AMP_DIFF)
UVD_AMP = randrange(2000-AMP_DIFF, 2000+AMP_DIFF)


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

    output = [0] * 10

    # Scale UVA data to a 16-bit resolution
    uva = twos_comp(uva)
    uvd = twos_comp(uvd)
    uvb = twos_comp(uvb)
    uvc1 = twos_comp(uvc1)
    uvc2 = twos_comp(uvc2)

    # Convert integers to binary form, to extract their LSB and MSB [0:7] and [8:15]
    uva_bin = bin(uva)[2:]
    uvd_bin = bin(uvd)[2:]
    uvb_bin = bin(uvb)[2:]
    uvc1_bin = bin(uvc1)[2:]
    uvc2_bin = bin(uvc2)[2:]

    # Set output bytes for UV data
    output[0] = uva_bin[8:15]
    output[1] = uva_bin[0:7]
    output[2] = uvd_bin[8:15]
    output[3] = uvd_bin[0:7]
    output[4] = uvb_bin[8:15]
    output[5] = uvb_bin[0:7]
    output[6] = uvc1_bin[8:15]
    output[7] = uvc1_bin[0:7]
    output[8] = uvc2_bin[8:15]
    output[9] = uvc2_bin[0:7]

    return output
