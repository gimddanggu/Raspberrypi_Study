import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# form_class 객체 생성
# ui 형태를 객체로 변환
form_class = uic.loadUiType("desi1.ui")[0]

class WindowClass(QDialog, form_class):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

	def event_handler_name(self): pass

if __name__  == "__main__":
	app = QApplication(sys.argv)
	myWindow  = WindowClass()
	myWindow.show()
	app.exec_()

