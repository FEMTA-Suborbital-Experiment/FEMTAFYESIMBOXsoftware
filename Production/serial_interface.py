# Module for handling serial interactions with the Arduino

import serial
from datetime import datetime

def StartSerialForwarding(serial_dev):
    while True:
        if serial_dev.in_waiting > 0:
            raw_line = serial_dev.read_until() # Read until a '\n' newline character
            try:
                line = raw_line.decode.rstrip() # Attempt to convert bytes to string
            except (UnicodeDecodeError):        # Invalid utf8 bytes in received sequence
                line = f"Raw Bytes {raw_line}"
            print(f"{datetime.now()} [SERIAL] >> {line}")

            if "processed" in line:
                pass # Add handling for command processing validation later