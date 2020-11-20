from busio import I2C
import board
import time
import RPi.GPIO as GPIO
import math

RED, GRN = 21, 13
address = 0x28 #DAC #1
reg0 = 0x0 #channel 0
reg1 = 0x1 #channel 1
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)

i2c = board.I2C()

try:
    i = 0
    GPIO.output(GRN, GPIO.HIGH)
    while True:
        msg0 = math.floor(127 * (math.cos(i/100) + 1))
        msg1 = math.floor(127 * (math.sin(i/100) + 1))
        i2c.writeto(address, bytes([reg0, msg0, reg1, msg1]))
        i += 1
        time.sleep(0.001)
except IOError as e:
    GPIO.output(RED, GPIO.HIGH)
    GPIO.output(GRN, GPIO.LOW)
    raise e
finally:
    GPIO.output(RED, GPIO.LOW)
    GPIO.output(GRN, GPIO.LOW)