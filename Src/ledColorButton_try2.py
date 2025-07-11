# 처음 작성했던 코드는 while 1 문까지 도달하지 못했다.
# 이유눈 exec_() 동작 방식에 있는데 
# 이 함수 또한 무한루프라고 볼 수 있다. 이 함수는 이벤트를 기다리면서 이벤트를 만나면 처리해주는 
# 역할을 한다. 따라서 처음 클래스가 생성된 이후로 while문이 실행되므로 exec_() 이벤트가 끝나지 않는 이상 
# while 문에 도달할 수 없어 led는 결과적으로 켜지지 않는 현상이 발생했다. 
# 이 문제를 해결하기 위해서는 핀 설정을 WindowClass init() 함수에 추가하고 
# while 문에서 동작하는 것들을  WindowClass 내의 함수로 따로 작성을 하던지(1), 기존 setGreen().. 등의 함수에 넣어주어야(2) 한다. 

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
		# 이 부분에서 문제 발생 - 나눗셈 방법 좋지않음
		c = int(c[2:])
		GPIO.output(self.b, c//100)
		GPIO.output(self.r, (c%100)//10)
		GPIO.output(self.g, c%100)
		# print(c//100, (c%100)//10, c%100)



class WindowClass(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		uic.loadUi("designer3.ui", self)
		
		self.BLUE = 14
		self.RED = 15
		self.GREEN = 18

		self.btn_flag = 0

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.BLUE, GPIO.OUT)
		GPIO.setup(self.RED, GPIO.OUT)
		GPIO.setup(self.GREEN, GPIO.OUT)

		self.c = Color(self.BLUE, self.RED, self.GREEN)
		self.show();

	def setBlue(self):
		self.label.setStyleSheet("color: blue;")
		self.btn_flag = 1

		color = 7 & self.btn_flag
		self.c.setColor(bin(color))
		print(f"Blue: 001 res:{int(bin(color)[2:])}")


	def setRed(self):
		self.label.setStyleSheet("color: red;")
		self.btn_flag = 2

		color = 7 & self.btn_flag
		self.c.setColor(bin(color))
		
		print(f"Red: 010 res:{int(bin(color)[2:])}")



	def setGreen(self):

		self.label.setStyleSheet("color: green;")
		self.btn_flag = 4

		color = 7 & self.btn_flag
		self.c.setColor(bin(color))
		print(f"Green: 100 res:{int(bin(color)[2:])}")


if __name__ == "__main__":
	app = QApplication(sys.argv)
	myWin = WindowClass()
	app.exec_()



