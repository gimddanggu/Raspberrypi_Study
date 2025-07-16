import RPi.GPIO as GPIO
import time

relayPin = 25

green = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)
#GPIO.setup(blue, GPIO.OUT)
#GPIO.setup(green, GPIO.OUT)

try:
	while True:
		GPIO.output(relayPin, True)
		print("BLUE")
		time.sleep(1)

		GPIO.output(relayPin, False)
		print("greeen")
#		GPIO.output(green, 1)
		time.sleep(1)
		GPIO.output(green, 0)

except KeyboardInterrupt:
	GPIO.cleanup()
		

