import sys
import cv2
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

path ='./chart-1.png'
written = []
with open("../src/wintermute_written.txt", "r") as f:
    for line in f:
        written.append(line.strip())



class Reader():
    def __init__(self):
        self.grid_labels={}
        self.choosen = ''
        
    def getdata(self,chart,rec,ws):
        self.chart = chart
        self.rec = rec
        self.WS = ws
    def calcRowHeight(self):
        img = cv2.imread(path,0)
        img = cv2.resize(img,(self.w,self.h))
        ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(30,1))
        result = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
        ret,labels,rowStats,centroids = cv2.connectedComponentsWithStats(~result,connectivity=4,ltype=cv2.CV_32S)
        self.rowStats = rowStats[1:]
        self.rowPos = [block[1] for block in self.rowStats if block[3] > 12]
        self.rowHeight = [block[3] for block in self.rowStats if block[3] > 12]
        self.rowCount = len(self.rowPos)
        if self.WS == False:
            self.total_row = self.rowCount*2
        else:
            self.total_row = self.rowCount
        self.hmean = round(self.h/len(self.rowPos))
        return
    def choose_grid(self,x,y):
        for abbr in self.rec.keys():
            for p in self.rec[abbr]:
                if p[0]<=x and x<=p[2] and p[1]<=y and y <= p[3]:
                    #print(abbr)
                    if(self.choosen):
                        self.clear_grid()
                    self.draw_grid(abbr)
                    return
    def draw_grid(self,abbr):
        if(abbr in self.grid_labels.keys()):
            for g in self.grid_labels[abbr]:
                g.show()
        else:
            self.grid_labels[abbr]=[]
            for grid in self.rec[abbr]:
                label = QLabel(self.form)
                x = round(grid[0]*self.patternLabel.width()/self.original[0])+self.patternLabel.x()
                y = round(grid[1]*self.patternLabel.height()/self.original[1])+self.patternLabel.y()
                w = round((grid[2]-grid[0])*self.patternLabel.width()/self.original[0])
                h = round((grid[3]-grid[1])*self.patternLabel.height()/self.original[1])
                label.setGeometry(x,y,w,h)
                op = QGraphicsOpacityEffect()
                op.setOpacity(0.25)
                label.setGraphicsEffect(op)
                label_img = QPixmap('./icon/gray.png').scaled(w,h)
                label.setPixmap(label_img)
                label.show()
                self.grid_labels[abbr].append(label)
        self.display_choice.setText(abbr)
        self.choosen=abbr
    def clear_grid(self):
        for label in self.grid_labels[self.choosen]:
            label.hide()
        self.grid_labels={}
        self.display_choice.setText("")
        self.choosen=''

    def drawBar(self):
        self.bar = QPixmap('./icon/blue_bar.png').scaled(self.w,self.hmean)
        self.pink_bar = QPixmap('./icon/pink_bar.png').scaled(self.w,self.hmean)
        self.barLabel = QLabel(self.form)
        self.barLabel.setPixmap(self.bar)
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.5)
        self.barLabel.setGraphicsEffect(op)
        #self.grid.addWidget(self.barLabel,0,0,wid,wid)
        self.barLabel.setGeometry(10,self.rowPos[self.pos]+10,self.bar.width(),self.rowHeight[self.pos])
        self.pointer = QLabel(self.form)
        self.pointer.setText(str(self.row))
        self.pointer.setFont(QFont('inconsolata',round(self.hmean/2.5)))
        self.pointer.setGeometry(self.w+20,self.rowPos[self.pos]+10,self.hmean,self.rowHeight[self.pos])
    
    def setBar(self):
        self.row = self.rowCount-self.pos
        
        if self.WS == False:
            if self.now %2 == 0:
                self.now = 2*self.row-1
            else:
                self.now = 2*(self.row-1)
            if self.now == 0:
                self.now = self.total_row
        else:
            self.now = self.row
        print(self.now,self.row)
        #self.rowLabel.setText(str(self.row))
        #self.patternText.setText(written[self.row-1])
        #print(self.WS,self.now)
        if self.WS == False and self.now%2 == 0:
            self.barLabel.setGeometry(self.barLabel.x(),self.rowPos[(self.pos+1)%self.rowCount]+5,self.barLabel.width(),10)
            self.pointer.setGeometry(self.pointer.x(),self.rowPos[(self.pos+1)%self.rowCount]-(self.hmean//2),self.pointer.width(),self.rowHeight[self.pos])
            self.patternText.setText("Row "+str(self.now))
        else:
            self.barLabel.setGeometry(self.barLabel.x(),self.rowPos[self.pos]+10,self.barLabel.width(),self.rowHeight[self.pos])
            self.pointer.setGeometry(self.pointer.x(),self.rowPos[self.pos]+10,self.pointer.width(),self.rowHeight[self.pos])
            self.patternText.setText("Row "+str(self.now)+": "+self.chart[self.row-1])
        if self.now%2==0:
            self.barLabel.setPixmap(self.pink_bar)
        else:
            self.barLabel.setPixmap(self.bar)
        self.pointer.setText(str(self.now))
    
        
        
        
    def incRow(self):
        if self.now%2 == 1 or self.WS:
            self.pos = (self.pos+self.rowCount-1)%self.rowCount
        self.setBar()
        return

    def decRow(self):
        if self.now %2 == 0 or self.WS:
            self.pos = (self.pos+1)%self.rowCount
        self.setBar()
        return
    
    def setStitch(self,num):
        if self.stitches==0 and num<0:
            return
        self.stscount.setText(str(self.stitches+num))
        self.stitches+=num
    def detect(self,event):
        if event.button() == 1:
            self.choose_grid(round(event.x()/self.patternLabel.width()*self.original[0]),round(event.y()/self.patternLabel.height()*self.original[1]))
    def detect_onbar(self,event):
        self.choose_grid(round((self.barLabel.x()+event.x())/self.patternLabel.width()*self.original[0])-self.patternLabel.x(),round((self.barLabel.y()+event.y())/self.patternLabel.height()*self.original[1])-self.patternLabel.y())
    def initUI(self,app):
        self.app = app
        self.screen = QApplication.desktop()
        self.form = QWidget()
        self.img = QPixmap(path)
        self.ratio = min(self.screen.width()/self.img.width(),self.screen.height()/self.img.height())
        self.h = round(self.img.height()*self.ratio*0.8)
        self.w = round(self.img.width()*self.ratio*0.8)
        self.original = [self.img.width(),self.img.height()]
        self.img = self.img.scaled(self.w,self.h)
        self.calcRowHeight()

        self.patternLabel = QLabel(self.form)
        self.patternLabel.setGeometry(10,10,self.w,self.h)
        self.patternLabel.setPixmap(self.img)
        
        self.pos=self.rowCount-1
        self.row = 1
        self.now = 1
        imagePath = ['./icon/cdd.png','','./icon/kfbf.png','./icon/cdd.png','./icon/kfbf.png','./icon/yo.png']
        textSet = ['+','','-','^','v','x']
        QFontDatabase.addApplicationFont("./font/Inconsolata-VariableFont_wdth,wght.ttf")
        self.buttons = [QPushButton(self.form) for i in range(len(imagePath))]
        for i in range(len(imagePath)):
            pos=i*(self.hmean+10)+25
            self.buttons[i].setGeometry(self.w+self.hmean+20,pos,self.hmean,self.hmean)
            #self.buttons[i].setIcon(QIcon(imagePath[i]))
            self.buttons[i].setText(textSet[i])
        
        self.stitches = 0
        self.buttons[0].clicked.connect(lambda: self.setStitch(1))
        self.buttons[1].hide()
        self.buttons[2].clicked.connect(lambda: self.setStitch(-1))
        self.buttons[3].clicked.connect(self.incRow)
        self.buttons[4].clicked.connect(self.decRow)
        #self.buttons[5].clicked.connect(QCoreApplication.instance().quit)
        self.buttons[5].clicked.connect(self.clear_grid)
        self.stscount = QLabel(self.form)
        self.stscount.setText(str(self.stitches))
        self.stscount.setFont(QFont('inconsolata',round(self.hmean/2.5)))
        self.stscount.move(self.w+self.hmean+20,self.buttons[1].y())
        
        self.display_choice = QLabel(self.form)
        self.display_choice.setFont(QFont('inconsolata',round(self.hmean/2.5)))
        self.display_choice.setAlignment(Qt.AlignCenter)
        self.display_choice.setGeometry(self.w+10,6*(self.hmean+10)+25,100,self.hmean)
        self.patternText = QLabel(self.form)
        self.stscount.setFont(QFont('inconsolata',round(self.hmean/2.5)))
        self.stscount.move(self.w+self.hmean+20,self.buttons[1].y())
        self.patternText.setFont(QFont('inconsolata',round(self.hmean/4)))
        self.patternText.setGeometry(10,self.h+10,self.w,self.hmean)
        self.patternText.setText("Row 1: "+self.chart[0])
        
        self.drawBar()
        self.form.resize(self.hmean*3+self.w,self.h+75)
        self.form.show()

        self.patternLabel.mousePressEvent = self.detect
        self.barLabel.mousePressEvent = self.detect_onbar
    def data_empty(self,app):
        #TODO: back button
        self.app = app
        self.form = QWidget()
        self.form.resize(1000,100)
        self.form.show()
        self.error_label = QLabel(self.form)
        self.error_label.setText("Error! Data must not be empty.")
        self.error_label.move(10,10)
        self.error_label.setFont(QFont('Arial',24))
        self.error_label.show()
        
if __name__ == '__main__':
    reader = Reader()
    app = QApplication(sys.argv)
    reader.initUI(app)
    sys.exit(app.exec_())