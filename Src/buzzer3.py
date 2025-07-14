import RPi.GPIO as GPIO
import time
import threading

piezoPin = 18
buttonPin = 15
blue = 23
red = 24


GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(piezoPin, GPIO.OUT)
GPIO.setup(blue, GPIO.OUT)
GPIO.setup(red, GPIO.OUT)


sound = GPIO.PWM(piezoPin, 440)

prePressTime = 0.0
waitInputTime = 0.8

cnt = 0

siren_active = False
siren_thread = None

def startyelp():
	print("yelp")
	for freq in range(800, 1600, 100):
		sound.ChangeFrequency(freq)
		time.sleep(0.03)
	for freq in range(160, 800, -100):
		sound.ChangeFrequency(freq)
		time.sleep(0.03)

def siren():
	global siren_active
	led_state = True
	
	while siren_active:
		for freq in range(600, 1600, 20):
			sound.ChangeFrequency(freq)

			if led_state:
				GPIO.output(blue, GPIO.LOW)
				GPIO.output(red, GPIO.HIGH)
			else:
				GPIO.output(blue, GPIO.HIGH)
				GPIO.output(red, GPIO.LOW)

			led_state = not led_state
			time.sleep(0.01)
			
		for freq in range(1600, 600, -20):
			sound.ChangeFrequency(freq)

			if led_state:
				GPIO.output(blue, GPIO.LOW)
				GPIO.output(red, GPIO.HIGH)
			else:
				GPIO.output(blue,GPIO.HIGH)
				GPIO.output(red, GPIO.LOW)
			led_state = not led_state
			time.sleep(0.01)

def start_siren():
	global siren_active, siren_thread
	if not siren_active:
		siren_active = True
		sound.start(50)
		siren_thread = threading.Thread(target=siren)
		siren_thread.start()

def stop_siren():
	global siren_active
	if siren_active:
		siren_active = False
		sound.stop()

try:
	while True:
		if GPIO.input(buttonPin) == GPIO.LOW:
			currTime = time.time()
			if currTime - prePressTime <= waitInputTime:
				print("press two")
				stop_siren()
				cnt = 0
		
			else:
				print("one press")
				start_siren()
				cnt = 1
				prePressTime = currTime
				
			time.sleep(0.3)
		
except KeyboardInterrupt:
	GPIO.cleanup()

			
