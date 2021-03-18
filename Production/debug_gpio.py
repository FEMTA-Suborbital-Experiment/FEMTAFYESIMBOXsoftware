# Stand-in GPIO class for debug mode testing

from smbx_logging import Logger

class GPIO:
    IN = "in"
    OUT = "out"
    HIGH = True
    LOW = False
    _pins = dict()

    @classmethod
    def setup(cls, pin_num, mode):
        cls._pins[pin_num] = mode

    @classmethod
    def input(cls, pin):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.IN:
            new_state = cls.HIGH #TODO: how do we chose GPIO input?
            with Logger("Debug") as log:
                log.write(f"GPIO {pin} input {'high' if new_state else 'low'}", "low_freq.txt")
            return new_state

    @classmethod
    def output(cls, pin, state):
        if pin in cls._pins.keys() and cls._pins[pin] == cls.OUT:
            with Logger("Debug") as log:
                log.write(f"GPIO {pin} output {'high' if state else 'low'}", "low_freq.txt")
