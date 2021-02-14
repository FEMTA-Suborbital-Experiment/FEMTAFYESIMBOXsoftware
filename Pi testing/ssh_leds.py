# Little test script to test running a python script from a remote ssh command
# Turns on the green LED for 1 second and echos sys.argv to stdout

import time
import sys
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT) #usual location for green LED indicator
GPIO.output(13, GPIO.HIGH)

try:
    for i in range(1000):
        with open("state","r") as f:
            r = f.read()
            print(r)
            if r[0] == "1":
                break
            else:
                time.sleep(0.01)
        if i == 999:
            print("Didn't work.")
finally:
    GPIO.output(13, GPIO.LOW)
    GPIO.cleanup()

#print(" ".join(sys.argv[1:]))