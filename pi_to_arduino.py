import serial
import time

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    data = range(256).__iter__()
    
    s.flush()  # This prevents other inputs except msg
    while True:
        s.write(bytes([data.__next__()]))
        output = s.readline()
        print(output)
        time.sleep(1)