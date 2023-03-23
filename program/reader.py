import tkinter.filedialog
import sys
import cv2
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import math
   
path ='./program/wintermute_cropped.png'
written = []
with open("./src/wintermute_written.txt", "r") as f:
    for line in f:
        written.append(line.strip())

class Reader():
    def __init__(self,WS):     
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        self.WS = WS
        self.app = QApplication(sys.argv)
        self.initUI()
    
    def calcRowHeight(self,w,h):
        img = cv2.imread(path,0)
        img = cv2.resize(img,(w,h))
        ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(30,1))
        result = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
        ret,labels,rowStats,centroids = cv2.connectedComponentsWithStats(~result,connectivity=4,ltype=cv2.CV_32S)
        self.rowStats = rowStats[1:]
        self.rowPos = [block[1] for block in self.rowStats if block[3] > 12]
        self.rowHeight = [block[3] for block in self.rowStats if block[3] > 12]
        self.rowCount = len(self.rowPos)
        self.hmean = round(h/len(self.rowPos))
        return
    
    
    def drawBar(self,w):
        self.bar = QPixmap('./program/blue_bar.png').scaled(w,self.hmean)
        self.pink_bar = QPixmap('./program/pink_bar.png').scaled(w,self.hmean)
        self.barLabel = QLabel(self.form)
        self.barLabel.setPixmap(self.bar)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.barLabel.setGraphicsEffect(op)
        #self.grid.addWidget(self.barLabel,0,0,wid,wid)
        self.barLabel.setGeometry(10,self.rowPos[self.pos]+10,self.bar.width(),self.rowHeight[self.pos])
        self.pointer = QLabel(self.form)
        self.pointer.setText(str(self.row))
        self.pointer.setFont(QFont('arial',round(self.hmean/1.75)))
        self.pointer.setGeometry(w+20,self.rowPos[self.pos]+10,self.hmean,self.rowHeight[self.pos])
    
    def setBar(self):
        self.row = (self.rowCount-self.pos)
        #self.rowLabel.setText(str(self.row))
        self.patternText.setText(written[self.row-1])
        if self.WS == True:
            if self.row%2==0:
                self.barLabel.setPixmap(self.pink_bar)
            else:
                self.barLabel.setPixmap(self.bar)
        self.barLabel.setGeometry(self.barLabel.x(),self.rowPos[self.pos]+10,self.barLabel.width(),self.rowHeight[self.pos])
        self.pointer.setText(str(self.row))
        self.pointer.setGeometry(self.pointer.x(),self.rowPos[self.pos]+10,self.pointer.width(),self.rowHeight[self.pos])
    def incRow(self):
        self.pos = (self.pos+self.rowCount-1)%self.rowCount
        self.setBar()
        return

    def decRow(self):
        self.pos = (self.pos+1)%self.rowCount
        self.setBar()
        return
    
    def setStitch(self,num):
        if self.stitches==0 and num<0:
            return
        self.stscount.setText(str(self.stitches+num))
        self.stitches+=num

    def initUI(self):
        self.screen = QApplication.desktop()
        self.form = QWidget()
        self.img = QPixmap(path)
        self.ratio = min(self.screen.width()/self.img.width(),self.screen.height()/self.img.height())
        h = round(self.img.height()*self.ratio*0.8)
        w = round(self.img.width()*self.ratio*0.8)
        self.img = self.img.scaled(w,h)
        self.calcRowHeight(w,h)

        self.patternLabel = QLabel(self.form)
        self.patternLabel.setGeometry(10,10,w,h)
        self.patternLabel.setPixmap(self.img)
        
        self.pos=self.rowCount-1
        self.row = 1
        
        imagePath = ['./src/cdd.png','','./src/kfbf.png','./src/cdd.png','./src/kfbf.png','./src/yo.png']
        self.buttons = [QPushButton(self.form) for i in range(len(imagePath))]
        for i in range(len(imagePath)):
            pos=i*(self.hmean+10)+25
            self.buttons[i].setGeometry(w+self.hmean+20,pos,self.hmean,self.hmean)
            self.buttons[i].setIcon(QIcon(imagePath[i]))
        
        self.stitches = 0
        self.buttons[0].clicked.connect(lambda: self.setStitch(1))
        self.buttons[1].hide()
        self.buttons[2].clicked.connect(lambda: self.setStitch(-1))
        self.buttons[3].clicked.connect(self.incRow)
        self.buttons[4].clicked.connect(self.decRow)
        self.buttons[5].clicked.connect(QCoreApplication.instance().quit)

        self.stscount = QLabel(self.form)
        self.stscount.setText(str(self.stitches))
        self.stscount.setFont(QFont('arial',round(self.hmean/1.5)))
        self.stscount.move(w+self.hmean+20,self.buttons[1].y())
        
        self.patternText = QLabel(self.form)
        self.patternText.setText(written[0])
        self.patternText.setFont(QFont('arial',round(self.hmean/2)))
        self.patternText.setGeometry(10,h+10,w,self.hmean)
        
        self.drawBar(w)
        self.form.resize(w+75,h+75)
        self.form.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Reader(True)