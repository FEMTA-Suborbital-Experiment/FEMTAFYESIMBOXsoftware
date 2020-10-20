import serial
import time

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    data = [0,1,2,3,4,5,6,7,8,9]
    i = 0
    
    s.flush()  # This prevents other inputs except msg
    while True:
        s.write(data[i])
        i += 1
        output = s.readline()
        print(output)
        time.sleep(1)