import tkinter.filedialog
import sys
import cv2
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import numpy as np
import math
   

class Reader():
    def __init__(self):     
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        self.app = QApplication(sys.argv)
        self.initUI()
        
    def calcRowHeight(self):
        img = cv2.imread('./program/cropped.png',0)
        ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(30,1))
        result = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
        ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~result,connectivity=4,ltype=cv2.CV_32S)
        stats = stats[2:]
        blockHeight=[]
        for block in stats:
            x,y,w,h,area = block
            blockHeight.append(h)
        self.hmean = math.floor(np.mean(blockHeight))
        return
    
    
    def drawBar(self,w):
        self.bar = QPixmap('./program/bar.png')
        self.bar = self.bar.scaled(w,self.hmean)
        self.barLabel = QLabel()
        self.barLabel.setPixmap(self.bar)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.barLabel.setGraphicsEffect(op)
        self.grid.addWidget(self.barLabel,0,0,10,10)
        
        
    def initUI(self):
        self.screen = QApplication.desktop()
        self.form = QWidget()
        self.img = QPixmap('./program/cropped.png')
        self.ratio = min(self.screen.width()/self.img.width(),self.screen.height()/self.img.height())
        h = round(self.img.height()*self.ratio*0.8)
        w = round(self.img.width()*self.ratio*0.8)
        self.calcRowHeight()
        self.img = self.img.scaled(w,h)
        self.patternLabel = QLabel()
        self.patternLabel.setPixmap(self.img)

        self.box=QWidget(self.form)
        self.box.setGeometry(0,0,w+75,h+75)

        self.grid = QGridLayout(self.box)
        self.grid.addWidget(self.patternLabel,0,0,20,20)

        self.inc = QPixmap('./src/cdd.png')
        self.inc = self.inc.scaled(self.hmean,self.hmean)
        self.incLabel = QLabel()
        self.incLabel.setPixmap(self.inc)
        self.grid.addWidget(self.incLabel,0,10)
        
        self.stscount = QLabel()
        self.stscount.setText("OAO")
        self.stscount.setStyleSheet('''
            font-size: 30px;
        ''')
        self.grid.addWidget(self.stscount,1,10)


        self.dec = QPixmap('./src/kfbf.png')
        self.dec= self.dec.scaled(self.hmean,self.hmean)
        self.decLabel = QLabel()
        self.decLabel.setPixmap(self.dec)
        self.grid.addWidget(self.decLabel,2,10)


        self.rowup = QPixmap('./src/cdd.png')
        self.rowup = self.rowup.scaled(self.hmean,self.hmean)
        self.rowupLabel = QLabel()
        self.rowupLabel.setPixmap(self.rowup)
        self.grid.addWidget(self.rowupLabel,3,10)

        self.rowdown = QPixmap('./src/kfbf.png')
        self.rowdown = self.rowdown.scaled(self.hmean,self.hmean)
        self.rowdownLabel = QLabel()
        self.rowdownLabel.setPixmap(self.rowdown)
        self.grid.addWidget(self.rowdownLabel,4,10)
        
        self.button = QPixmap('./src/yo.png')
        self.buttonLabel = QLabel()
        self.buttonLabel.setPixmap(self.button)
        self.buttonLabel.setAlignment(Qt.AlignRight)
        self.grid.addWidget(self.buttonLabel,5,10)
        
        self.drawBar(w)
        self.form.resize(w+75,h+75)
        self.form.show()
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    Reader()