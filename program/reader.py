import tkinter, tkinter.filedialog
import sys
import cv2
import os
from PyQt5 import QtWidgets,QtGui
from PyQt5.QtGui import *

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()

form = QtWidgets.QWidget()
layout =QtWidgets.QVBoxLayout(form)
form.resize(300,300)

class Reader:
    def __init__(self):     
        pattern = QtWidgets.QGraphicsView(form)
        pattern.setGeometry(20,20,220,300)
        scene = QtWidgets.QGraphicsScene()
        scene.setSceneRect(0,0,220,300)
        img = QtGui.QPixmap('test_image1.png')
        img = img.scaled(220,300)
        scene.addPixmap(img)
        pattern.setScene(scene)
        #form.resize(420,700)
        form.show()
        sys.exit(app.exec_())



if __name__ == '__main__':
    Reader()