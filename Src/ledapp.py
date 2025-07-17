from flask import Flask, request, render_template
import RPi.GPIO as GPIO

app = Flask(__name__)

ledPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)

@app.route('/')
def home():
	return render_template("index.html")

@app.route('/data', methods=['POST'])
def date():
	data = request.form['led']
	if data == 'on':
		GPIO.output(ledPin, GPIO.HIGH)
	else:
		GPIO.output(ledPin, GPIO.LOW)
	return render_template("index.html")

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=4567)
