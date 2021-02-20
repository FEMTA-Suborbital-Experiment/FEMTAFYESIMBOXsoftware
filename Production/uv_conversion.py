# Functions to generate meaningless UV sensor data (sinusoids) and to
# convert that data to the expected format

# It seems we don't need the UVD channel, so all that's commented out for now,
# but could in theory be re-implemented later (with changes to the Arduino code)

from math import sin
from random import randrange
from common_library import twos_comp, sine_generator

STEP_SIZE = 0.1
AMP_DIFF = 200


UVA_AMP = randrange(8000-AMP_DIFF, 8000+AMP_DIFF)
UVB_AMP = randrange(10000-AMP_DIFF, 10000+AMP_DIFF)
UVC1_AMP = randrange(3200-AMP_DIFF, 3200+AMP_DIFF)
UVC2_AMP = randrange(4700-AMP_DIFF, 4700+AMP_DIFF)
#UVD_AMP = randrange(2000-AMP_DIFF, 2000+AMP_DIFF)


def sine_generator(step_size, amplitude):
    x = 0
    while True:
        yield amplitude + amplitude * sin(x)
        x += step_size


uva = sine_generator(STEP_SIZE, UVA_AMP)
uvb = sine_generator(STEP_SIZE, UVB_AMP)
uvc1 = sine_generator(STEP_SIZE, UVC1_AMP)
uvc2 = sine_generator(STEP_SIZE, UVC2_AMP)
#uvd = sine_generator(STEP_SIZE, UVD_AMP)


def make_fake_uv(state):
    if state == 0: #normal
        #return next(uva), next(uvb), next(uvc1), next(uvc2), next(uvd)
        return (next(uva), next(uvb), next(uvc1), next(uvc2))
    elif state == 1: #min
        #return (0, 0, 0, 0, 0)
        return (0, 0, 0, 0)
    elif state == 2: #max
        #return (UVA_AMP, UVB_AMP, UVC1_AMP, UVC2_AMP, UVD_AMP)
        return (UVA_AMP, UVB_AMP, UVC1_AMP, UVC2_AMP)

def uv_conversion(uva, uvb, uvc1, uvc2, uvd):
    
    output = [0] * 8    # Arduino expects 8 bytes of data values (4 * 2-byte pairs)

    # Scale UVA data to a 16-bit resolution
    uva = twos_comp(int(uva))
    #uvd = twos_comp(int(uvd))  where did this come from? UV sensor only has A, B, C1, and C2
    uvb = twos_comp(int(uvb))
    uvc1 = twos_comp(int(uvc1))
    uvc2 = twos_comp(int(uvc2))

    #Format into high and low bytes
    output[0:2] = divmod(uva, 256)[::-1]    # Reverse so data is in little endian order [lo, hi] = (remainder, quotient)
    #output[2:4] = divmod(uvd, 256)
    output[2:4] = divmod(uvb, 256)[::-1]
    output[4:6] = divmod(uvc1, 256)[::-1]
    output[6:8] = divmod(uvc2, 256)[::-1]

    return output
