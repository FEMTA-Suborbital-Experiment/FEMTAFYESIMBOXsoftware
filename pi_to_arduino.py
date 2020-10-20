import serial
import time


if __name__ == '__main__':
    s = serial.Serial('/dev/serial0', baudrate=115200, timeout=1)

    msg = b'Hello from the Raspberry pi'

    s.flush()  # This prevents other inputs except msg
    while True:
        s.write(msg)
        output = s.readline().decode()
        print(output)
        time.sleep(1)
