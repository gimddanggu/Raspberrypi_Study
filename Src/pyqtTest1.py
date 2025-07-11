import sys
from PyQt5.QtWidgets import QApplication, QWidget

# 파이썬에서 괄호안은 상속이라는 의미
class MyApp(QWidget):
	def __init__(self):	# 생성자
		super().__init__() # 부모 생성자 호출
		self.initUi()

	def initUi(self):
		self.setWindowTitle("My First Application")
		self.move(300, 300) # 위젯 이동 
		self.resize(400, 200) # 크기 변경
		self.show()

# 이 파일을 실행할 것인지 모듈을 사용할 것인지 모듈로 사용할 경우 파일이름이된다.
if __name__ == "__main__":
	app = QApplication(sys.argv)
	ex = MyApp()
	sys.exit(app.exec_())