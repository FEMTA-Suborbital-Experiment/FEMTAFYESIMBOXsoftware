# Stand-in GPIO class for debug mode testing

import time
from .smbx_logging import Logger

class GPIO:
    IN = "in"
    OUT = "out"
    HIGH = True
    LOW = False
    BCM = 0
    _pins = dict() #pin number : input/output pairs
    _state = dict() #pin number : on/off (for outputs obviously)
    _start_t = time.time() #not exactly correct, but good enough

    @classmethod
    def setup(cls, pin_num, mode):
        cls._pins[pin_num] = mode

    @classmethod
    def _get_new_state(cls, pin):
        # Outline of events; O = open, C = close (timeline from matlab source)
        # flow1:-----------O------------------------------
        # flow2: ----------O------------C-----------------
        #  vent: -----------------------------------------
        # times:           |168.385     |200.000
        
        time_diff = time.time() - cls._start_t
        if pin == 23 or pin == 10: #open flow sol 1 or flow sol 2
            return cls.HIGH if 168.385 <= time_diff < 168.635 else cls.LOW
        elif pin == 9: #close flow sol 2
            return cls.HIGH if 200 <= time_diff < 200.25 else cls.LOW
        else:
            return cls.LOW

    @classmethod
    def input(cls, pin):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.IN:
            new_state = cls._get_new_state(pin)
            with Logger("debug") as log:
                log.write(f"GPIO {pin} read {'high' if new_state else 'low'}", "gpio_debug.txt")
            return new_state

    @classmethod
    def output(cls, pin, state):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.OUT:
            with Logger("debug") as log:
                log.write(f"GPIO {pin} write {'high' if state else 'low'}", "low_freq.txt")

    @classmethod
    def setmode(cls, mode):
        pass
