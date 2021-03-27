# Module for handling serial interactions with the Arduino

import time
import multiprocessing as mp
from .smbx_logging import Logger

COMMAND_LEN = 27

class ArduinoI2CSimInterface(mp.Process):
    # 0s timeout means read is non-blocking and returns buffered bytes immediately,
    # None timeout means wait until requested bytes or terminator character received
    def __init__(self, port, baudrate=115200, timeout=None, debug=False):
        # Init super class (multiprocessing Process)
        mp.Process.__init__(self, name='ArduinoI2CSimInterface', daemon=True)
        
        self.log = Logger("arduino")
        self.log.start()
        self.debug = debug

        if not self.debug:
            import serial # Import moved here for debug mode flexibility

            self.log.write("Initializing serial object", "low_freq.txt", True)
            self.sp = serial.Serial(baudrate=baudrate, timeout=timeout)
            self.sp.port = port # Initialize port separately so serial port does not open immediately
        
        else:
            self.debug_log = Logger("debug")
            self.debug_log.start()
            self.debug_log.write("Skipping actual initialization of serial object", "low_freq.txt", True)

        self.processed = mp.Event() # Event sync primitive to verify a command has been processed

    """
    The Arduino performs a reset whenever a new connection to the serial port is established. It
    takes a few seconds for it to complete this, at which point the first thing it does is send
    a message down the port signaling that it is ready. This should be run after establishing the
    serial port and before any other operations involving the Arduino.
    """
    # Establish serial port connection and wait for Arduino to respond
    def connect(self, timeout=5.0):
        if not self.debug:
            self.log.write("Waiting for Arduino on serial port", "low_freq.txt", True, end='', flush=True)
            self.sp.open()  # Connect to Arduino over serial port, triggering reset
            self.sp.flush()
            t_start = time.time()
            while self.sp.in_waiting == 0:
                if time.time() - t_start > timeout:
                    raise ConnectionError("Waiting for Arduino over serial port timed out")
                print(".", end='', flush=True)
                time.sleep(0.5) # Don't hog the processor busywaiting
            print()
            self.log.write("Arduino has signaled ready", "low_freq.txt", True)
        else:
            self.debug_log.write("Skipping acquisition of actual serial connection", "low_freq.txt", True)
        
        self.processed.set()

    # Method overload for multiprocessing Process, is started in new process when .start() is called
    def run(self):
        if not self.debug:
            if not self.sp.is_open:
                raise ConnectionError("Arduino serial port is not open")

            while self.sp.is_open:
                if self.sp.in_waiting > 0:
                    raw_line = self.sp.read_until()     # Read until a '\n' newline character
                    try:
                        line = raw_line.decode().rstrip()   # Attempt to convert bytes to string
                    except UnicodeDecodeError:            # Invalid utf8 bytes in received sequence
                        line = f"Raw Bytes: {raw_line}"
                    
                    self.log.write(f"SERIAL >> {line}", "arduino.txt")
                    if "processed" in line:
                        self.processed.set()

            raise ConnectionError("Arduino serial port closed unexpectedly")
        else:
            self.debug_log.write("Entering serial handling loop...", "low_freq.txt", True)
            while True:
                time.sleep(0.001)
                if not self.processed.is_set():
                    self.debug_log.write("Setting command processing complete flag", "arduino.txt")
                    self.processed.set()

    # Method to send a command out to the Arduino
    def sendCommand(self, command):
        # Validate command
        if not isinstance(command, (tuple, list, bytes)):
            raise TypeError("Command must be a tuple or list of values, or raw bytes")
        if len(command) != COMMAND_LEN:
            raise ValueError(f"Commands must be {COMMAND_LEN} values or bytes")

        if self.processed.is_set(): # Last command is processed, good to send another
            cmd = bytes(command)
            cmd_str = f"{' '.join(f'{b:#04x}' for b in cmd)}"
            if self.debug:
                self.debug_log.write(cmd_str, "arduino.txt")
                sent = cmd
            else:
                self.log.write(cmd_str, "arduino.txt")
                sent = self.sp.write(cmd)
            self.processed.clear()
        else:
            self.log.write("WARNING: Arduino over serial port is not ready to receive another command", "low_freq.txt", True)
            sent, cmd = None, None
        
        return sent, cmd

    # Close the serial port
    def close(self):
        if not self.debug:
            self.sp.close()
        self.processed.clear()

        self.log.close()
        if self.debug:
            self.debug_log.close()

        mp.Process.terminate(self)
