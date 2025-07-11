import sys
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
#label = QLabel("Hello PyQt!!")
label = QPushButton("Quit")
label.show()
app.exec()
