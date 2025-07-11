import RPi.GPIO as GPIO
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class Color():
	def __init__(self, b, r, g):
		self.b = b
		self.r = r
		self.g = g

	def setColor(self, c):
		c = int(c[2:])
		GPIO.output(BLUE, c//100)
		GPIO.output(RED, (c%100)//10)
		GPIO.output(GREEN, c%100)



class WindowClass(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		uic.loadUi("designer3.ui", self)
		self.show();

	def setBlue(self):
		global btn_flag
		self.label.setStyleSheet("color: blue;")
		btn_flag = 1

	def setRed(self):
		global btn_flag
		self.label.setStyleSheet("color: red;")
		btn_flag = 2

	def setGreen(self):
		global btn_flag
		self.label.setStyleSheet("color: green;")
		btn_flag = 4

if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWin = WindowClass()
	app.exec_()


BLUE = 14
RED = 15
GREEN = 18

btn_flag = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(BLUE, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

c = Color(0, 0, 0)

while 1:
	try:
		if btn_flag:
			color = 7 & btn_flag
			c.setColor(bin(color))
			print(color)
	except KeyboardInterrupt:
		GPIO.cleanup()
