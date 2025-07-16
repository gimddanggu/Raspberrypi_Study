from flask import Flask
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

bluePin = 14
redPin = 15
greenPin = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)



@app.route('/')
def hello():
	return "LedControl"

@app.route('/led/<state>')
def led(state):
	if state == "red":
		GPIO.output(redPin, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(redPin, GPIO.LOW)
	elif state == "blue":
		GPIO.output(bluePin, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(bluePin, GPIO.LOW)
	elif state == "green":
		GPIO.output(greenPin, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(greenPin, GPIO.LOW)
		
	return "LED" + state

@app.route('/led/clean')
def gpioCleanup():
	GPIO.cleanup()
	return "<H1>GPIO CLEANUP</H1>"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

# from flask import Flask
# import RPi.GPIO as GPIO
# import time
# app = Flask(__name__)

# ledPin1 = 14 # blue
# ledPin2= 15 # red
# ledPin3 = 18 # green
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(ledPin1, GPIO.OUT)
# GPIO.setup(ledPin2, GPIO.OUT)
# GPIO.setup(ledPin3, GPIO.OUT)


# @app.route('/')
# def ledFlask():
# 	return "LED Control Web"

# @app.route('/led/<state>')
# def led(state):
# 	if state == 'blue':
# 		GPIO.output(ledPin1, GPIO.HIGH)
# 		time.sleep(1)
# 		GPIO.output(ledPin1, GPIO.LOW)

# 	elif state == 'red':
# 		GPIO.output(ledPin2, GPIO.HIGH)
# 		time.sleep(1)
# 		GPIO.output(ledPin2, GPIO.LOW)
	
# 	elif state == 'green':
# 		GPIO.output(ledPin3, GPIO.HIGH)
# 		time.sleep(1)
# 		GPIO.output(ledPin3, GPIO.LOW)

# 	return "LED" + state
	
# @app.route('/led/clean')
# def gpiocleanup():
# 	GPIO.cleanup()
# 	return "<H1>GPIO CLEANUP</H1>"

# if __name__ == "__main__":
# 	app.run(host='0.0.0.0')
