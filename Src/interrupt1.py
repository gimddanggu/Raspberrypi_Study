# Interrupt 실습2 - 버튼 눌렀다 떼면 초록 led 출력

import RPi.GPIO as GPIO
import time
swPin = 14
bluePin = 16
redPin = 20
greenPin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
startTime = 0.0

def callback(channel):
	print("LED ON!!!")
	GPIO.output(greenPin, 1)
	time.sleep(1)
	GPIO.output(greenPin, 0)

	
GPIO.add_event_detect(swPin, GPIO.RISING, callback=callback, bouncetime=200)

try:
	while True:
		time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()
