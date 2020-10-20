import serial
import time


if __name__ == '__main__':
    s = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    msg = 420

    s.flush()  # This prevents other inputs except msg
    while True:
        s.write(msg)
        output = s.readline()
        print(output)
        time.sleep(0.2)
