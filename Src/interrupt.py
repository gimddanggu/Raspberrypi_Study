import RPi.GPIO as GPIO
import time

# 인터럽트 실습1 - 인터럽트 맛보기
swPin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def printcallback(channel):
	print("pushed")

GPIO.add_event_detect(swPin, GPIO.RISING, callback=printcallback, bouncetime=200)

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
	
