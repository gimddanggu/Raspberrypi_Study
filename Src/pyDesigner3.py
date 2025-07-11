import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

class WindowClass(QDialog):
	def __init__(self, parent = None):
		super().__init__(parent)
		uic.loadUi("designer2.ui", self)
		self.show()
	def slot1(self):
		self.label.setText("left btn clicked")
	def slot2(self):
		self.label.setText("right btn clicked")

if __name__ == "__main__":
	app = QApplication(sys.argv)
	exc = WindowClass()
	app.exec_()
