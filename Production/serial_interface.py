# Module for handling serial interactions with the Arduino

import serial
import multiprocessing as mp
import time
from datetime import datetime, timedelta

COMMAND_LEN = 27

class ArduinoI2CSimInterface(mp.Process):

    def __init__(self, port, baudrate=115200, timeout=None):
        # Init super class (multiprocessing Process)
        mp.Process.__init__(self, name='ArduinoI2CSimInterface', daemon=True)
        self.sp = serial.Serial(baudrate=baudrate, timeout=timeout)
        self.sp.port = port # Initialize port separately so serial port does not open immediately

        self.processed = mp.Event() # Event sync primitive to verify a command has been processed

    """
    The Arduino performs a reset whenever a new connection to the serial port is established. It
    takes a few seconds for it to complete this, at which point the first thing it does is send
    a message down the port signaling that it is ready. This should be run after establishing the
    serial port and before any other operations involving the Arduino.
    """
    # Establish serial port connection and wait for Arduino to respond
    def connect(self, timeout=5.0):
        print("Waiting for Arduino on serial port", end='', flush=True)
        self.sp.open()  # Connect to Arduino over serial port, triggering reset
        self.sp.flush()
        t_start = datetime.now()
        t_delta = timedelta(seconds=timeout)
        while self.sp.in_waiting == 0:
            if datetime.now() - t_start > t_delta:
                raise ConnectionError("Waiting for Arduino over serial port timed out")
            print(".", end='', flush=True)
            time.sleep(0.5) # Don't hog the processor busywaiting
        print("\nArduino has signaled ready")
        self.processed.set()
        return

    # Method overload for multiprocessing Process, is started in new process when .start() is called
    def run(self):
        if not self.sp.is_open:
            raise ConnectionError("Arduino serial port is not open")

        while self.sp.is_open:
            if self.sp.in_waiting > 0:
                raw_line = self.sp.read_until()     # Read until a '\n' newline character
                try:
                    line = raw_line.decode().rstrip()   # Attempt to convert bytes to string
                except (UnicodeDecodeError):            # Invalid utf8 bytes in received sequence
                    line = f"Raw Bytes {raw_line}"
                
                if "processed" in line:
                    self.processed.set()
                    print(f"{datetime.now()} [SERIAL] >> {line}", flush=True) # Send to both if split
                else:
                    print(f"{datetime.now()} [SERIAL] >> {line}", flush=True) # Send this to a different stream to prevent clogging?

        raise ConnectionError("Arduino serial port closed unexpectedly")

    # Method to send a command out to the Arduino
    def sendCommand(self, command):
        # Validate command
        if not isinstance(command, (tuple, list, bytes)):
            raise TypeError("Command must be a tuple or list of values, or raw bytes")
        if len(command) != COMMAND_LEN:
            raise ValueError(f"Commands must be {COMMAND_LEN} values or bytes")

        if self.processed.is_set(): # Last command is processed, good to send another
            cmd = bytes(command)
            print(f"Sending command {' '.join(f'{b:#04x}' for b in cmd)}")
            sent = self.sp.write(cmd)
            self.processed.clear()
        else:
            raise RuntimeWarning("Arduino over serial port is not ready to recieve another command")
        
        return sent, cmd

    # Close the serial port
    def close(self):
        self.sp.close()
        self.processed.clear()
        mp.Process.terminate(self)
