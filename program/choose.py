import tkinter, tkinter.filedialog
import sys
import cv2
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from pdf2image import convert_from_path
from skimage.measure import label as tag
import numpy as np
import recognition

class Choose:
    def __init__(self): 
        self.app = QtWidgets.QApplication(sys.argv)

        self.form = QtWidgets.QWidget()
        self.form.resize(420,700)

        self.btn = QtWidgets.QPushButton(self.form)
        self.btn.setText("Select Pattern")
        self.btn.clicked.connect(self.getPath)

        self.now_page=1
        self.total_page=1
        self.scr_count = 0
    
        self.init_pos = [-1,-1]
        self.drawing=False

        self.form.show()
        self.rec = recognition.Transfer()
        sys.exit(self.app.exec_())

    def getPath(self):
        window = tkinter.Tk()
        window.withdraw()     
        self.file_path = tkinter.filedialog.askopenfilename(parent=window,title='Select File', filetypes=(("application/pdf","*.pdf"),("all files","*.*")))
        self.convert()

    def convert(self):
        #convert image
        """images = convert_from_path(self.file_path,300,poppler_path=r'C:\Program Files\poppler-0.67.0\bin') #DPI
        for i, image in enumerate(images):
            fname = 'test_image'+str(i+1)+'.png' #path
            image.save(fname, "PNG")"""
        self.choose()

    def choose(self):
        self.check_total_page()
        self.pixmap = QtGui.QPixmap('test_image'+str(self.now_page)+'.png').scaled(420,594)
        
        self.label = QtWidgets.QLabel(self.form)
        self.label.setGeometry(0,50,420,600)

        imagePath = ['./program/left.png','./program/right.png','./program/rotate.png','']
        self.btns = [ QtWidgets.QPushButton(self.form) for i in range(4)]
        for i in range(4):
            self.btns[i].setGeometry(100*i,0,100,50)
            self.btns[i].setIcon(QIcon(imagePath[i]))
            self.btns[i].show()
        self.btns[3].setText("Select")
        self.btns[0].clicked.connect(self.page_up)
        self.btns[1].clicked.connect(self.page_down)
        self.btns[2].clicked.connect(self.rotate)
        self.btns[3].clicked.connect(self.select)
        self.wsCheckbox = QtWidgets.QCheckBox(self.form)
        self.wsCheckbox.setGeometry(10,650,25,25)
        self.wsCheckbox.show()
        self.wsCheckbox.clicked.connect(self.changeState)
        self.WS = False
        self.wsTextLabel = QtWidgets.QLabel(self.form)
        self.wsTextLabel.setText("There are WS rows in pattern.")
        self.wsTextLabel.setGeometry(45,650,500,25)
        self.wsTextLabel.show()
        self.display()
    def changeState(self):
        self.WS = not self.WS
        self.rec.setWS(self.WS)
    def page_down(self):
        if(self.now_page < self.total_page):
            self.now_page+=1
            self.pixmap = QtGui.QPixmap('test_image'+str(self.now_page)+'.png').scaled(420,594)
            self.display()
    def page_up(self):
        if(self.now_page>1):
            self.now_page-=1
            self.pixmap = QtGui.QPixmap('test_image'+str(self.now_page)+'.png').scaled(420,594)
            self.display()

    def rotate(self):
        transform = QtGui.QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        if (self.label.height()==600):
            self.label.setGeometry(0,50,594,420)
            self.form.resize(594,600)
        else:
            self.label.setGeometry(0,50,420,600)
            self.form.resize(420,700)
        self.display()

    def select(self):
        self.img = cv2.imread('test_image'+str(self.now_page)+'.png')
        cv2.namedWindow('image',0)
        cv2.resizeWindow('image',420,594)
        cv2.setMouseCallback('image',self.draw)
        cv2.imshow('image',self.img)
        self.scr_count+=1

    def display(self):
        self.label.setPixmap(self.pixmap)
        self.label.show()
        self.form.show()

    def draw(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing=True
            self.init_pos = [x,y]
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                img2 = self.img.copy() 
                cv2.rectangle(img2, (self.init_pos[0],self.init_pos[1]),(x,y), (0,0,255), 10)
                cv2.imshow('image',img2)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.screenshot = self.img[self.init_pos[1]:y,self.init_pos[0]:x]
            #cv2.imwrite(str(self.scr_count)+'.png',self.screenshot)
            self.crop(self.screenshot)
            
    def check_total_page(self):
        while os.path.exists('test_image'+str(self.total_page)+'.png'):
            self.total_page+=1
        return
            
    def crop(self,screenshot):
        self.img = cv2.cvtColor(screenshot,cv2.COLOR_BGR2GRAY)
        img =  cv2.threshold(self.img,250,255,cv2.THRESH_BINARY_INV)[1]
        labeled,num=tag(img,background=0,return_num=True)
        max_label=0
        max_num=0
        for i in range(1,num+1):
            sub_num = np.sum(labeled==i)
            if sub_num>max_num:
                max_num=sub_num
                max_label=i
        if max_label>0:
            img[labeled!=max_label]=0
        gray = 255*(img < 128).astype(np.uint8)
        coords = cv2.findNonZero(~gray)
        x, y, w, h = cv2.boundingRect(coords)
        rect = self.img[y:y+h,x:x+w]
        cv2.imwrite('rect.png',rect)
        print(y,y+h,x,x+w)
        self.rec.process(rect)
        return
if __name__ == '__main__':
    Choose()