import tkinter, tkinter.filedialog
import sys
import cv2
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from pdf2image import convert_from_path

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.resize(420,594)
form = QtWidgets.QWidget()
label = QtWidgets.QLabel(window)
layout =QtWidgets.QVBoxLayout(form)

init_pos = [-1,-1]
drawing=False
scr_count = 0

class Choose: 
    now_page=1
    #改total_page
    total_page=0
    file_path = ""
    def __init__(self):     
        btn = QtWidgets.QPushButton(form)
        btn.setText("Select Pattern")
        btn.clicked.connect(self.getPath)
        form.show()
        sys.exit(app.exec_())
    def getPath(self):
        window = tkinter.Tk()
        window.withdraw()     
        self.file_path = tkinter.filedialog.askopenfilename(parent=window,title='Select File', filetypes=(("application/pdf","*.pdf"),("all files","*.*")))
        #print(file_path)
        self.convert()
    def convert(self):
        images = convert_from_path(self.file_path,300,poppler_path=r'C:\Program Files\poppler-0.67.0\bin') #DPI
        for i, image in enumerate(images):
            fname = 'test_image'+str(i+1)+'.png' #path
            self.total_page+=1
            image.save(fname, "PNG")
        self.choose()
    def choose(self):
        self.check_total_page()
        form.resize(420,700)
        btnup = QtWidgets.QPushButton(form)
        btnup.setText(">")
        btnup.clicked.connect(self.page_down)
        btnup.move(200,0)
        btnup.show()
        btndn = QtWidgets.QPushButton(form)
        btndn.setText("<")
        btndn.clicked.connect(self.page_up)
        btndn.move(100,0)
        btndn.show()
        btncon = QtWidgets.QPushButton(form)
        btncon.setText("Confirm")
        btncon.clicked.connect(self.select)
        btncon.move(300,0)
        btncon.show()
        self.display()
    def page_down(self):
        if(self.now_page < self.total_page):
            self.now_page+=1
            self.display()
    def page_up(self):
        if(self.now_page>1):
            self.now_page-=1
            self.display()
    def display(self):
        original = cv2.imread('test_image'+str(self.now_page)+'.png')
        img = cv2.resize(original,(210*2,297*2))
        height,width,channel = img.shape
        bytesperline = channel * width
        qimg = QImage(img, width,height,bytesperline,QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap(420,594).fromImage(qimg)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        form.resize(420,700)
    def select(self):
        global img, original, scr_count
        original = cv2.imread('test_image'+str(self.now_page)+'.png')
        img = cv2.resize(original,(210*2,297*2))
        cv2.namedWindow('image',0)
        cv2.resizeWindow('image',420,594)
        cv2.setMouseCallback('image',self.draw)
        cv2.imshow('image',img)
        scr_count+=1
    def draw(self,event,x,y,flags,param):
        global init_pos, drawing, scr_count
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing=True
            init_pos = [x,y]
        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                img2 = img.copy() 
                cv2.rectangle(img2, (init_pos[0],init_pos[1]),(x,y), (0,0,255), 2)
                cv2.imshow('image',img2)
        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            print(scr_count,init_pos,x,y)
            #times = original.shape[0]/(297*2)
            #cv2.imwrite('.\source\screenshot\\'+str(scr_count)+'.png',original[int(init_pos[1]*times):int(y*times),int(init_pos[0]*times):int(x*times)])
            #cv2.imwrite('.\source\screenshot\\'+str(scr_count)+'.png',img[init_pos[1]:y,init_pos[0]:x])
            cv2.imwrite(str(scr_count)+'.png',img[init_pos[1]:y,init_pos[0]:x])
    def check_total_page(self):
        page = 1
        while True:
            if os.path.exists('.\\test_image'+str(page)+'.png'):
                self.total_page=page
                page+=1
            else:
                return

if __name__ == '__main__':
    Choose()