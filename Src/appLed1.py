from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)

ledPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

@app.route('/')
def helloFlask():
	return "Hello Flak"

@app.route('/led/on')
def LedRed():
	GPIO.output(ledPin, GPIO.HIGH)
	return "<h1> LED ON </h1>"

@app.route('/led/off')
def LedOff():
	GPIO.output(ledPin, GPIO.LOW)
	return "<h1> LED OFF </h1>"

if __name__ == "__main__":
	app.run(host='0.0.0.0', port="8080")
	
