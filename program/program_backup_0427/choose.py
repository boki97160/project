import tkinter, tkinter.filedialog
import sys
import cv2
import os, glob
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from pdf2image import convert_from_path
from skimage.measure import label as tag
import numpy as np
import recognition, reader
import fitz

class Choose:
    
    def __init__(self,app):
        self.app = app #QApplication(sys.argv)
        self.screen = QApplication.desktop()
        self.rec = recognition.Transfer()
        self.reader = reader.Reader()
        self.form = QWidget()
        self.init_data()
        #sys.exit(self.app.exec_())
    
    def init_data(self):
        self.h = self.screen.height()-300
        self.w = round(self.h*210/297)
        self.form.resize(self.w,self.h+175)
        self.selectPattern()
        
        self.now_page=1
        self.total_page=1
        self.chart_count = 0
        self.init_pos = [-1,-1]
        self.drawing=False
        self.rotated = 0
        self.changed = False
        self.form.show()
                
    def selectPattern(self):
        self.btn = QPushButton(self.form)
        self.btn.setText("Select Pattern")
        #self.btn.setFont(QFont('inconsolata',12))
        self.btn.setStyleSheet('''
            QPushButton{
                font-size: 12px;
                font-family: inconsolata;
            }
            QPushButton:hover{
                border: 3px solid black
            }
        ''')
        self.btn.setGeometry(int(self.form.width()/2)-50, int(self.form.height()/2)-60, 100, 50)
        self.btn.clicked.connect(self.getPath)
    
    def getPath(self):
        window = tkinter.Tk()
        window.withdraw()     
        self.file_path = tkinter.filedialog.askopenfilename(parent=window,title='Select File', filetypes=(("application/pdf","*.pdf"),("all files","*.*")))
        if not self.file_path:
            self.Label = QLabel('You do not select any files. Please select again.', self.form)
            self.Label.setFont(QFont('inconsolata',10))
            self.Label.move(100, int(self.form.height()/2))
            self.Label.show()
            return
        self.btn.hide()
        self.convert()
    
    def convert(self): # pdf 轉成 一頁一頁
        #convert image
        #images = convert_from_path(self.file_path,300,poppler_path=r'C:\Program Files\poppler-0.67.0\bin') #DPI       
        self.path_name = self.file_path.split('/')
        
        files = glob.glob('test_image*.png') # 把之前紀錄刪掉
        if files:
            for file in files:
                os.remove(file)

        """for i, image in enumerate(images):
            fname = 'test_image'+str(i+1)+'.png' #path
            image.save(fname, "PNG")"""
        
        doc = fitz.open(self.file_path)
        for page_index in range(doc.page_count):
            page = doc.load_page(page_index)  
            pix = page.get_pixmap(dpi=300)
            nppix = np.frombuffer(buffer=pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
            fname = 'test_image'+str(page_index+1)+'.png'
            cv2.imwrite(fname,cv2.cvtColor(nppix,cv2.COLOR_RGB2BGR))

        self.choose()
    
    def back(self):
        self.btn.show()
        for i in range(self.btns_num):
            self.btns[i].setParent(None)
        self.wsCheckbox.setParent(None)
        self.wsTextLabel.setParent(None)
        self.label.setParent(None)
        self.init_data()
        self.selectPattern()
    
    def next(self):
        #TODO :change to input.py 
        self.rec.process(self.app,self.WS,self.path_name[-1][:-4])
        self.form.hide()
    
    def choose(self):
        self.check_total_page()
        self.pixmap = QPixmap('./test_image'+str(self.now_page)+'.png')
        if self.pixmap.width()>self.pixmap.height():
            self.w, self.h = self.h, self.w 
            self.form.resize(self.w,self.h+175)
        self.pixmap = self.pixmap.scaled(self.w,self.h)
        self.label = QLabel(self.form)
        self.label.setGeometry(0,50,self.w,self.h)
        textSet = ['<','>','⟳','Select Chart','Select Key','< Back','Next >']
        self.btns_num = len(textSet)
        self.btns = [ QPushButton(self.form) for i in range(self.btns_num)]
        for i in range(self.btns_num):
            self.btns[i].setText(textSet[i])
            self.btns[i].setStyleSheet('''
                QPushButton{
                    font-size:12px;
                    font-family: inconsolata;
                }
                QPushButton:hover{
                    color:red;
                    border: 2px solid black;
                }
            ''')
            self.btns[i].show()
        for i in range(self.btns_num-2):
            self.btns[i].setGeometry(round(self.w/(self.btns_num-2)*i),0,round(self.w/(self.btns_num-2)),50)
            
        for i in (self.btns_num-2,self.btns_num-1):
            self.btns[i].setGeometry(round(self.w/(self.btns_num-2)*(i-2)),self.h+100,round(self.w/(self.btns_num-2)),50)
        self.btns[0].clicked.connect(self.page_up)
        self.btns[1].clicked.connect(self.page_down)
        self.btns[2].clicked.connect(lambda x : self.rotate("button"))
        self.btns[3].clicked.connect(lambda x : self.select("chart"))
        self.btns[4].clicked.connect(lambda x : self.select("key"))
        self.btns[5].clicked.connect(self.back)
        self.btns[6].clicked.connect(self.next)
        self.wsCheckbox = QCheckBox(self.form)
        self.wsCheckbox.setGeometry(10,self.h+50,25,25)
        self.wsCheckbox.show()
        self.wsCheckbox.clicked.connect(self.changeState)
        self.WS = False
        self.wsTextLabel = QLabel(self.form)
        self.wsTextLabel.setText("There are WS rows in pattern.")
        self.wsTextLabel.setGeometry(45,self.h+50,500,25)
        self.wsTextLabel.show()
        self.display()
    def changeState(self):
        self.WS = not self.WS
    def page_down(self):
        if(self.now_page < self.total_page):
            self.now_page+=1       
            self.pixmap = QPixmap('./test_image'+str(self.now_page)+'.png').scaled(self.w,self.h)
            if self.rotated % 2==1:
                self.rotate("pgdn")
                self.changed = True
                self.pixmap = QPixmap('./test_image'+str(self.now_page)+'.png').scaled(self.w,self.h)
            self.rotated = 0
            self.display()
    def page_up(self):
        if(self.now_page>1):
            self.now_page-=1
            
            self.pixmap = QPixmap('./test_image'+str(self.now_page)+'.png').scaled(self.w,self.h)
            if self.rotated % 2==1:
                self.rotate("pgup")
                self.changed = True
                self.pixmap = QPixmap('./test_image'+str(self.now_page)+'.png').scaled(self.w,self.h)
            self.rotated = 0
            self.display()

    def rotate(self,source):
        if source == "button":
            self.rotated= (self.rotated+1)%4
            self.changed = False
        self.h, self.w = self.w, self.h
        transform = QTransform().rotate(90)
        self.pixmap = self.pixmap.transformed(transform, Qt.SmoothTransformation)
        
        self.label.setGeometry(0,50,self.w,self.h)
        self.wsCheckbox.setGeometry(10,self.h+50,25,25)
        self.wsTextLabel.setGeometry(45,self.h+50,500,25)
        bt = self.btns_num-2
        self.btns[bt].setGeometry(round(self.w/bt*(bt-2)),self.h+100,round(self.w/bt),50)
        self.btns[bt+1].setGeometry(round(self.w/bt*(bt-1)),self.h+100,round(self.w/bt),50)
        self.form.resize(self.w,self.h+175)
        if source == "button":
            self.display()
    
    def select(self,source):
        self.img = cv2.imread('./test_image'+str(self.now_page)+'.png')
        cv2.namedWindow('image',0)
        cv2.resizeWindow('image',self.w,self.h)
        self.source = source
        cv2.setMouseCallback('image',self.draw)
        cv2.imshow('image',self.img)
        if self.source == "chart":
            self.chart_count+=1

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
            self.cropped = self.crop(self.screenshot)
            
    def check_total_page(self):
        while os.path.exists('./test_image'+str(self.total_page)+'.png'):
            self.total_page+=1
        self.total_page-=1
        return

    def crop(self,screenshot):
        self.img = cv2.cvtColor(screenshot,cv2.COLOR_BGR2GRAY)
        img =  cv2.threshold(self.img,250,255,cv2.THRESH_BINARY_INV)[1]
        if self.source == "chart":
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
        print(y,y+h,x,x+w)
        if self.source == "chart":
            #cv2.imwrite('chart-'+str(self.chart_count)+'.png',self.img[y:y+h,x:x+w])
            cv2.imwrite('chart.png',self.img[y:y+h,x:x+w])
            '''if y+h > 1000 :
                print('do this')
                replace = cv2.imread('chart-'+str(self.chart_count)+'.png',0)
                resize_h, resize_w= h*40/100, w*40/100
                replace = cv2.resize(replace, (int(resize_h), int(resize_w)))
                os.remove('chart-'+str(self.chart_count)+'.png')
                cv2.imwrite('chart-'+str(self.chart_count)+'.png', replace)'''

        elif self.source == "key":
            cv2.imwrite('key.png',self.img[y:y+h,x:x+w])

'''if __name__ == '__main__':
    Choose()'''