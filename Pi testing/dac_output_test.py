# Script to test the DAC chip that electronics has. Sends a cos wave to
# channel 0 and a sin wave to channel 1. Should be pretty easily extensible
# to test more channels and the second DAC. Wiring should be done in accorrdance
# with our final plans for the Pi's pinout.

import board
import time
import RPi.GPIO as GPIO
import math

RED, GRN = 21, 13
ad0 = 0x28 #DAC 0 address
ad1 = 0x29 #DAC 1 address
reg0 = (0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7) #channels for DAC0
reg1 = (0x4, 0x5, 0x6, 0x7) #channels for DAC1
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)

i2c = board.I2C()

try:
    i = 0
    GPIO.output(GRN, GPIO.HIGH)
    while True:
        signal = math.floor(127 * (math.cos(i/100) + 1))
        msg0 = [signal if i % 2 else reg0[i//2] for i in range(16)] #signal, reg0, signal, reg1, etc for DAC0
        msg1 = [signal if i % 2 else reg1[i//2] for i in range(8)] #same for DAC1
        i2c.writeto(ad0, bytes(msg0))
        i2c.writeto(ad1, bytes(msg1))
        i += 1
        time.sleep(0.001)
except IOError as e:
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GRN, GPIO.LOW)
    time.sleep(1)
    raise e
finally:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GRN, GPIO.LOW)