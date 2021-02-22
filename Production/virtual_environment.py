# Start the virtual environment on a separate process through a class that inherits the multiprocessing Process
# class.
# Based on Mark Hartigan's multiprocessing implementation:
# https://github.com/purdue-orbital/avionics/blob/master/src/balloon.py
# This will determine how to start the virtual environment as a process. From Mark's implementation,
# however, I am thinking of writing this such that it runs as a function rather than a class.
# I have a simple idea of how I could do this, as __main__.py already imports multiprocessing.
# It makes running in a function consistent with the style of __main__.py et. al.

from multiprocessing import Process, Event
from config_parser import configs
from datetime import datetime
now = datetime.now

import Simulation.constants as const
import Simulation.helpers as helps

times = configs["event_times"]


class VirtualEnvironmentProcess(Process):
    def __init__(self):
        Process.__init__(self)
        self.exit = Event()

    def run(self, start_t):  # Run the virtual environment
        print("Virtual Environment Running")
        time = (now() - start_t).total_seconds()
        while time < max(times):
            # Virtual Environment Code
            print("BUZZZZ")

    def shutdown(self):  # Stop the virtual environment
        print("Killing Virtual Environment process")
        self.exit.set()
        print("Virtual Environment killed")

