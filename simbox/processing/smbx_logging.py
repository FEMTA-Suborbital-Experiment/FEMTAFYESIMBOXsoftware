# Purpose built logger for diagnostics and recording during simbox experiments.
# Works with context managers. If not using context managers, call start()
# (right) before using and close() when done.
#
# We should also keep track of what files we're using and what for:
#
# main_hf.csv      | Used by:
#    "main": High-frequency data (100 Hz) generated by main.py
# 
# low_freq.txt     | Used by:
#    "main" (main.py): Diagnostics and status updates, etc. Some msgs also printed
#    "simulation" (sim.py): Warning about desync
#    "debug" (i2c_interface.py, serial_interface.py, debug_gpio.py): 
#            Status updates. Some also printed.
#    "arduino" (serial_interface.py): Infrequent status updates
#    "I2C" (serial_interface.py): I2C locking function only
#
# arduino.txt      | Used by:
#    "arduino" (serial_interface.py): Data sent to and received from arduino
#    "debug" (serial_interface.py): Data that would be sent to arduino
#
# i2c_debug.txt    | Used by:
#    "debug" (i2c_interface.py): Every write to the debug I2C (high freq)
#
# gpio_debug.txt   | Used by:
#    "debug" (debug_gpio.py): Reads from simulated GPIO pins.

import os
import time

class Logger:
    
    instances = 0
    file_objects = dict()
    directory = f"/home/pi/Project_Files/experiment_logs/{time.strftime('%y-%m-%dT%H:%M')}/" # unique directory name per experiment
    os.mkdir(directory)

    def __init__(self, name):
        self.name = ascii(name)[1:-1]
        self.start_t = None

    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return None

    def start(self):
        Logger.instances += 1
        self.start_t = time.perf_counter()

    def close(self):
        Logger.instances -= 1
        if not Logger.instances: # No more active instances remaining, i.e. we're last to be shut down
            for fo in Logger.file_objects.values():
                fo.close()

    def write(self, text, filename, print_=False, **print_kwargs):
        assert self.start_t is not None, f"Logger \"{self.name}\" has not had start() called"

        if filename not in Logger.file_objects.keys():
            # open with mode x because we neither want to overwrite a 
            # previous log nor combine two logs together
            try:
                Logger.file_objects[filename] = open(Logger.directory + filename, "x", encoding="ascii")
            except FileExistsError as e:
                raise Exception(f"log file \"{filename}\" already exists") from e 
        
        Logger.file_objects[filename].write(f"{self.name} [T+{time.perf_counter() - self.start_t:.3f}]: {ascii(text)[1:-1]}\n")

        if print_:
            # Print logged message to terminal. These should be infrequent and
            # straightforward, so no need to include the logger name and time
            print(text, **print_kwargs)


if __name__ == '__main__':
    with Logger("main") as log1, Logger("arduino") as log2:
        print(log1.name, log2.name)
        log1.write("Hello World!", "test.txt")
        log2.write("Hello again", "test.txt", True)
        log1.write("Print kwargs:", "test.txt", True, end="<end str>\n")
