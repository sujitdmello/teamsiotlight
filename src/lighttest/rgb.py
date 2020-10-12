import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

RUNNING = True

red = 27
green = 17
blue = 22

GPIO.setup(red, GPIO.OUT)
GPIO.setup(green, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)

Freq = 100

RED = GPIO.PWM(red, Freq)
GREEN = GPIO.PWM(green, Freq)
BLUE = GPIO.PWM(blue, Freq)

try:
	RED.start(100)
	time.sleep(5)
	RED.start(0)
	GREEN.start(100)
	time.sleep(5)
	GREEN.start(0)
	BLUE.start(100)
	time.sleep(5)
	# Yellow color = R + G
	BLUE.start(0)
	RED.start(100)
	GREEN.start(100)
	time.sleep(5)
	RUNNING = False
	BLUE.start(0)
	RED.start(0)
	GREEN.start(0)
	GPIO.cleanup()
	exit()

except KeyboardInterrupt:
#the purpose of this part is, when you interrupt the code, it will stop the while loop and turn off the pins, which means your LED won't light anymore
	RUNNING = False
	GPIO.cleanup()