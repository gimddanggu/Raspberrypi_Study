import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

BUTTON = 17
BLUE = 14
RED = 15
GREEN = 18

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

try:
	while True:
		if GPIO.input(BUTTON):
			GPIO.output(BLUE, 1)
			GPIO.output(RED, 0)
			GPIO.output(GREEN, 1)

		else:
			GPIO.output(BLUE, 0)
			GPIO.output(RED, 0)
			GPIO.output(GREEN, 1)

except KeyboardInterrupt:
	GPIO.cleanup()
