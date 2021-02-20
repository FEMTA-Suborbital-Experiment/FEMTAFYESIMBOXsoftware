'''
rpi_flightcomputer_sim

Simulates the I2C commands sent to sensors for testing the I2C emulator code
while also providing commands over serial to the I2C emulator code.
'''

import board, busio # Circuitpython imports for I2C usage
import serial       # Serial port package
import colorama     # Used for colored formating of console text
from colorama import Fore, Back, Style
import time
from datetime import datetime
import random
from threading import Thread, Event
import os

ARDUINO_PORT = '/dev/ttyACM0'   # Change this depending on port Arduino appears on
BAUD_RATE = 115200              # Baud rate used for serial comms
LOGFILE = 'test_log.txt'        # Logging output file
TEST_INTERVAL = 1.0             # Number of seconds between tests
COMMAND_INTERVAL = 9.0          # Number of seconds between serial commands
ERR_STATE = 0b000               # Error state for address disabling
TEST_BADS = True                # Whether or not to test bad reads

working_dir = os.path.dirname(os.path.abspath(__file__))    # Get the parent directory

with busio.I2C(board.SCL, board.SDA) as i2c, serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=0.1) as sp,\
  open(os.path.join(working_dir, LOGFILE), 'w') as log:

    def log_print(s, end='', style=''): # Simple wrapper for printing/logging at the same time
        print_end = f'{Style.RESET_ALL}{end}'
        if style == '':
            print_end = end
        print(f"{style}{s}", end=print_end, flush=True)
        log.write(f'({datetime.now()}) {s}{end}')

    processed = Event() # Threading communication event
    def serialPortHandler():
        while sp.in_waiting > 0:   # Nonzero bytes in buffer
            raw_line = sp.readline()
            try:
                line = raw_line.decode().rstrip()   # Turn the line to text
            except:
                line = f"(Raw bytes) {raw_line}"
            log_print(f"[Serial]", '', f"{Back.WHITE + Fore.BLACK}")
            log_print(f" >> {line}", '\n')
            if 'processed' in line:
                processed.set()

    # Wrapper for attempting a function call multiple times
    def attemptTimes(func, *args, n=3, message=None, errstyle=f"{Back.RED + Fore.BLACK}", **kwargs):
        if message is None:
            message = f"Attempting to call {func} w/ args={args}, kwargs={kwargs}"

        failures = 0
        log_print(message, '\n')
        for i in range(1, n+1):
            log_print(f" ({i}/{n})\t")
            try:
                func(*args, **kwargs)
                log_print(f"Succeeded with {failures} failure(s)", '\n', f"{Back.GREEN + Fore.BLACK}")
                break
            except Exception as e:
                failures += 1
                log_print(f"Exception raised: {e} ", '\n', errstyle)

        return failures

    # Prepare serial port and wait for response
    sp.flush()

    log_print("Waiting on serial port")
    while sp.in_waiting == 0:
        log_print('.')
        time.sleep(0.5)

    log_print("\nSerial port awake!", '\n')

    try:
        log_print("Waiting on I2C lock")
        while not i2c.try_lock():
            log_print('.')
            time.sleep(0.5)
        log_print("\nI2C lock obtained!", '\n')

        now_time = time.time()
        next_command_time = now_time + 1.0
        next_test_time = now_time + 1.0

        # Making sure these exist before entering loop
        flow_1_data = None
        flow_2_data = None
        uv_data     = None

        # Enter loop to handle testing
        while True:
            now_time = time.time()
            serialPortHandler()

            # Code to handle testing cases
            if now_time >= next_command_time:
                next_command_time = now_time + COMMAND_INTERVAL

                # Produce random test data
                flow_1_data = [random.randint(0, 0xFF) for n in range(9)]
                flow_2_data = [random.randint(0, 0xFF) for n in range(9)]
                uv_data     = [random.randint(0, 0xFF) for n in range(8)]

                command = [ERR_STATE] + flow_1_data + flow_2_data + uv_data
                log_print(" Sending command:            " + ' '.join(f'{x:#04x}' for x in command) + '', '\n', f"{Back.CYAN + Fore.BLACK}")
                sp.write(bytes(command))
                processed.clear()

            # Waits until command has been processed
            if processed.is_set() and now_time >= next_test_time:
                next_test_time = now_time + TEST_INTERVAL

                # Empty data buffers for i2c reading
                flow_1_rx   = [0] * 9
                flow_2_rx   = [0] * 9
                uv_rx       = [0] * 8 + [0xFF] * 2  # Extra space to test reading a bad command

                # 2 flow sensors
                for device, buffer in zip((0x08, 0x09), (flow_1_rx, flow_2_rx)):
                    attemptTimes(i2c.readfrom_into, device, buffer, message=f"Attempting to read from flow sensor at {device:#04x}")
                    serialPortHandler()

                # Check the good reads for their results
                log_print(f"\n Comparing reads... ", '\n', f"{Back.GREEN + Fore.BLACK}")
                if flow_1_rx == flow_1_data:
                    log_print(" - Flow 1 checks out. ", '\n', f"{Back.GREEN + Fore.BLACK}")
                else:
                    log_print(f" - Flow 1 mismatch: {flow_1_data} vs {flow_1_rx} received. ", '\n', f"{Back.MAGENTA + Fore.BLACK}")
                if flow_2_rx == flow_2_data:
                    log_print(" - Flow 2 checks out. ", '\n', f"{Back.GREEN + Fore.BLACK}")
                else:
                    log_print(f" - Flow 2 mismatch: {flow_2_data} vs {flow_2_rx} received. ", '\n', f"{Back.MAGENTA + Fore.BLACK}")

                # UV sensor
                device = 0x10
                # 4 good commands + one bad command
                for uv_cmd, position in zip((0x07, 0x09, 0x0A, 0x0B, 0x0C), range(0, 10, 2)):
                    attemptTimes(i2c.writeto_then_readfrom, device, bytes((uv_cmd, )), uv_rx, in_start=position,
                        message=f"Attempting to read from uv sensor at {device:#04x} w/ command {uv_cmd:#04x}")
                    serialPortHandler()

                log_print(f"\n Comparing reads... ", '\n', f"{Back.GREEN + Fore.BLACK}")
                if uv_rx[:8] == uv_data:
                    log_print(f" - UV checks out. Last 2 bytes recieved was {uv_rx[8:]} ", '\n', f"{Back.GREEN + Fore.BLACK}")
                else:
                    log_print(f" - UV mismatch: {uv_data} vs {uv_rx} received. ", '\n', f"{Back.MAGENTA + Fore.BLACK}")
                
                # Make bad reads
                if TEST_BADS:
                    read_buffers = [[0xFF] * 10] * 4            # Temporary buffers to hold data trying to be read
                    read_devices = (0x00, 0x01, 0x0A, 0x18)     # Device addresses to test by reading
                    rw_buffers   = [[0xFF] * 10] * 4            # Temporary buffers to hold data trying to be read w/ a command
                    rw_devices   = (0x10, 0x11, 0x19, 0x1A)     # Device addresses to test by reading by command
                    
                    for device, buffer in zip(read_devices, read_buffers):
                        attemptTimes(i2c.readfrom_into, device, buffer, message=f"Attempting bad read of device at {device:#04x}",
                            errstyle=f"{Back.YELLOW + Fore.BLACK}")
                        log_print("Buffer data: " + ' '.join(f'{x:#04x}' for x in buffer), '\n')
                        serialPortHandler()
                    
                    for device, buffer in zip(rw_devices, rw_buffers):
                        attemptTimes(i2c.writeto_then_readfrom, device, bytes((uv_cmd, )), buffer,
                            message=f"Attempting bad read of device at {device:#04x} w/ command {uv_cmd:#04x}",
                            errstyle=f"{Back.YELLOW + Fore.BLACK}")
                        log_print("Buffer data: " + ' '.join(f'{x:#04x}' for x in buffer), '\n')
                        serialPortHandler()

            # End of response to sent serial command processed
        # Loop end
    finally:
        i2c.unlock()    # Release i2c lock when done


# Old stuff
'''
def serialPortLogger():
    print("Serial Logger started!")
    while True:
        if sp.in_waiting > 0:   # Nonzero bytes in buffer
            line = sp.readline().decode().rstrip()
            print(line, flush=True)

# Link I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Link Serial
sp = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1.0)
sp.flush()

while sp.in_waiting == 0:   # Wait until serial port wakes up
    pass

serial_thread = Thread(target=serialPortLogger, daemon=True)
serial_thread.start()

err_state = bytes((0x00, ))

print(f"{Back.RED + Fore.BLACK} Hello world {Style.RESET_ALL}")
time.sleep(2.0)

while True:
    # Generate a random command
    flow_1_data = bytes(random.randint(0, 0xFF) for n in range(9))
    flow_2_data = bytes(random.randint(0, 0xFF) for n in range(9))
    uv_data     = bytes(random.randint(0, 0xFF) for n in range(8))

    command = err_state + flow_1_data + flow_2_data + uv_data

    # Send the command
    print("Sending command", ' '.join(f'{b:#04x}' for b in command))
    # sp.flush()
    sp.write(command)
    # sp.flush()
    time.sleep(0.02)   # Wait a bit for the command to process

    # Poll for data
    # Empty data buffers for i2c reading
    flow_1_rx   = [0] * 9
    flow_2_rx   = [0] * 9
    uv_rx       = [0] * 8

    # 2 flow sensors
    for device, buffer in zip((0x08, 0x09), (flow_1_rx, flow_2_rx)):
        print(f"Reading from device {device:#04x}")
        try:
            i2c.readfrom_into(device, buffer)
        except OSError as e:
            print(f"Error reading device {device}: {e}")
        #time.sleep(0.5)

    # UV sensor
    device = 0x10
    for uv_cmd, position in zip((0x07, 0x09, 0x0A, 0x0B), range(0, 8, 2)):
        for i in range(3):
            print(f"Reading from device {device:#04x} with code {uv_cmd:#04x}")
            try:
                i2c.writeto_then_readfrom(device, bytes((uv_cmd, )), uv_rx, in_start=position, stop=True)
                break
            except OSError as e:
                print(f"{Back.RED + Fore.BLACK} Error reading device {device}: {e} {Style.RESET_ALL}")
                if i == 2:
                    print('Whoops!')
        #time.sleep(0.1)

    # Compare results
    print(f"Flow 1: {list(flow_1_data)} vs {flow_1_rx}")
    print(f"Flow 2: {list(flow_2_data)} vs {flow_2_rx}")
    print(f"UV    : {list(uv_data)} vs {uv_rx}")

    time.sleep(0.1)
'''