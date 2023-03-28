import sys,os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2

class Start():
    def __init__(self):
        super().__init__()
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        self.app = QApplication(sys.argv)        
        self.form = QWidget()
        self.label = QLabel(self.form)
        self.input = QLineEdit(self.form)
        self.input.setGeometry(0,0,100,self.input.height())
        self.next = QPushButton(self.form)
        self.next.clicked.connect(self.make)
        self.next.move(100,0)
        self.form.show()
        

        
        sys.exit(self.app.exec_())
    
    def make(self):
        text = self.input.text()
        if text == "":
            print("project name cannot be empty")
            return
        if os.path.exists(text):
            print("exist")
        else:
            self.form.hide()
            #os.makedirs('./data/'+text)
            #print("OAO")
            os.system("python choose.py")

if __name__ == '__main__':
    Start()
    
    