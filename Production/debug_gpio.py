# Stand-in GPIO class for debug mode testing

import time
from smbx_logging import Logger

class GPIO:
    IN = "in"
    OUT = "out"
    HIGH = True
    LOW = False
    _pins = dict()
    start_t = time.time() #not exactly correct, but good enough

    @classmethod
    def setup(cls, pin_num, mode):
        cls._pins[pin_num] = mode

    @classmethod
    def _get_new_state(cls, pin, t): #conditions taken from matlab source
        time_diff = time.time() - t
        if pin == 4: #first pin, we're calling it the first flow solenoid
            return cls.LOW if time_diff < 168.385 else cls.HIGH
        elif pin == 14: #second flow sol
            return cls.HIGH if 168.385 < time_diff < 200 else cls.LOW
        elif pin == 15: #vent sol
            return cls.HIGH
        else:
            return cls.LOW

    @classmethod
    def input(cls, pin):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.IN:
            new_state = cls._get_new_state(pin, time.time())
            with Logger("Debug") as log:
                log.write(f"GPIO {pin} input {'high' if new_state else 'low'}", "low_freq.txt")
            return new_state

    @classmethod
    def output(cls, pin, state):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.OUT:
            with Logger("Debug") as log:
                log.write(f"GPIO {pin} output {'high' if state else 'low'}", "low_freq.txt")
