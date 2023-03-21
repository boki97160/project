import sys,os
from PyQt5 import QtWidgets,QtGui

app = QtWidgets.QApplication(sys.argv)

class Start(QtWidgets.QWidget):
    def __init__(self):
        print("init")
        super().__init__()
        global input
        input = QtWidgets.QLineEdit(self)
        next = QtWidgets.QPushButton('Next',self)
        next.move(175,0)
        next.clicked.connect(self.make)
    def make(self):
        print("make")
        text = input.text()
        if os.path.exists(text):
            print("exist")
        else:
            os.makedirs(text)
            os.system('python choose.py')
