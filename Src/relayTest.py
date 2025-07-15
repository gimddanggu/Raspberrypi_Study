import RPi.GPIO as GPIO
import time

relayPin = 23


GPIO.setmode(GPIO.BCM)
GPIO.setup(relayPin, GPIO.OUT)

try:
	while True:
		GPIO.output(relayPin, True)
		print("True")
		time.sleep(1)

		GPIO.output(relayPin, False)
		print("False")
		time.sleep(1)

except KeyboardInterrupt:
	print("BYE")
finally:
	GPIO.cleanup()

