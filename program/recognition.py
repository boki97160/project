import tkinter.filedialog
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import numpy as np
from sewar.full_ref import ssim

pattern_name = "nurmilintu"
scale = 30

key_content = ["","k","k","k","p","k","kfb","k","yo","k","k2tog","k","ssk","k","sk2p","k"]

def find_stats(original, scale):
    src= cv2.threshold(original,250,255,cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
    result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
    result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    table = cv2.bitwise_or(result1,result2)
    stats= cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)[2][2:]
    return stats

def isBlank(grid):
    return np.count_nonzero(grid >=250)>grid.shape[0]*grid.shape[1]*0.95

class Key:
    def __init__(self,abbr,block,width):
        self.abbr = abbr
        self.width = width
        self.symbol = block

class Transfer:
    size = 0
    pattern = [] 
    key_list = [[] for i in range(20)]
    def __init__(self):
        self.read_keys()
        self.read_chart()
        self.split()
        self.traversal()
    def read_keys(self):
        original_keys = cv2.imread('./src/'+pattern_name+'_key.png',cv2.IMREAD_GRAYSCALE)
        keys = find_stats(original_keys,scale)
        key_count = 0
        for x,y,w,h,area in keys: 
            width = round(w/h)
            if width < 10: #small unwanted slice
                key = Key(key_content[key_count],original_keys[y:y+h,x:x+w],width)
                self.key_list[width].append(key)
                key_count+=1
    def read_chart(self):
        self.original_pattern = cv2.imread('./src/'+pattern_name+'_chart.png',cv2.IMREAD_GRAYSCALE)
        self.grid = find_stats(self.original_pattern,scale)
        self.size = round(np.mean(self.grid[:,3]))
    def split(self):
        tmp_list = []
        dist = 12
        last_y=-1
        for now in self.grid:
            x,y,w,h,area = now
            if(abs(y-last_y)>dist):
                last_y=y
                tmp_list.sort(reverse=True,key=lambda x:(x[0]))
                self.pattern.append(tmp_list)
                tmp_list=[]
            tmp_list.append(now)
        tmp_list.sort(reverse=True,key=lambda x:(x[0]))
        self.pattern.append(tmp_list)
        self.pattern = self.pattern[::-1]
    def traversal(self):
        for i in range(len(self.key_list)):
            for j in range(len(self.key_list[i])):
                self.key_list[i][j].symbol = cv2.resize(self.key_list[i][j].symbol,(self.size*self.key_list[i][j].width,self.size))
        print(self.key_list)
        f=open("./src/"+pattern_name+"_written.txt","r")
        row=1
        for i in range(len(self.pattern)):
            tmp_list=[]
            res=""
            for j in range(len(self.pattern[i])):
                x,y,w,h,area = self.pattern[i][j]
                g=self.original_pattern[y:y+h,x:x+w]         
                content = self.compare_grid(g)
                if content!="":
                    tmp_list.append(content) 
            if len(tmp_list)>0:
                written = f.readline()[:-1]
                res = str(row)+": "+', '.join(tmp_list)
                print(res)
                row+=1
                ws = written[3:].split(', ')
                for w in range(len(ws)):
                    if ws[w]!=tmp_list[w]:
                        print(ws[w]+" / "+tmp_list[w])
                print(res == written)
                #f.write(res+"\n")   
        f.close()
    def compare_grid(self,grid):
        if grid.shape[0]<0.8*self.size or grid.shape[1]<0.8*self.size:
            return ""
        if(isBlank(grid)):
            return "k"
        width = round(grid.shape[1]/grid.shape[0])
        return self.key_list[width][self.cmpsim(grid,width)].abbr
    #TODO: need to change into cosine distance
    def cmpsim(self,grid,width):
        grid = cv2.resize(grid,(self.size*width,self.size))
        sim = []
        for i in range(len(self.key_list[width])):
            sim.append(ssim(grid,self.key_list[width][i].symbol)[1])
        return np.argmax(sim)


Transfer()
#####


