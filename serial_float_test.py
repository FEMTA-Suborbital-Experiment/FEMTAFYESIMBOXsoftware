import serial
import time

"""NOTE: Python uses doubles for all floats (that we'll be using?)
   Apparently the best way to pass floats/doubles over serial is to
   convert them to strings. (Though that feels gross.)"""

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    data = [0.00, 1.11, 2.22, 3.33, 4.44, 5.55, 6.66, 7.77, 8.88, 9.99]
    data = [str(val).encode('utf-8') for val in data]
    
    s.flush()  # This prevents other inputs except msg
    for val in data:
        s.write(val)
        output = s.readline()
        try:
            print(output)
        except TypeError:
            pass
        time.sleep(1)