# event
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__() 
        self.initUi()

    def initUi(self):
        self.setWindowTitle("PyQt Button Test")
        self.move(300, 300)
        self.resize(400, 200)

        button = QPushButton("Click", self)
        button.move(20, 20)

        button.clicked.connect(self.button_clicked) # 이벤트와 위젯 연결 handeler: button_clicked

    def button_clicked(self):
        QMessageBox.about(self, "Message", "clicked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())