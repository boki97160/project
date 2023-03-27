import sys,os
from PyQt5 import QtWidgets,QtGui

from reader import *

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.resize(420,594)

form = QtWidgets.QWidget()
label = QtWidgets.QLabel(window)

layout =QtWidgets.QVBoxLayout(form)
layout.addWidget(label)

class Start(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.input = QtWidgets.QLineEdit(self)
        next = QtWidgets.QPushButton('Next',self)
        next.move(175,0)
        next.clicked.connect(self.make)
    def make(self):
        text = self.input.text()
        if os.path.exists(text):
            print("exist")
        else:
            os.makedirs('.//program/data/'+text)
            os.system('python .//program//choose.py')

if __name__ == '__main__':
    Start()