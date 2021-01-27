# Test run on the Pi. Sends out three bytes at a time, over
# serial, every half second.

import serial
import time

if __name__ == '__main__':
    s = serial.Serial('/dev/ttyACM0', baudrate=115200, timeout=1)
    data = [[i,i+1,i+2,0 if i<100 else 2] for i in range(0,256,3)]
    s.flush()  # This prevents other inputs except msg
    
    try:
        for trip in data:
            s.write(bytes(trip))
            time.sleep(0.5)
    except:
        pass