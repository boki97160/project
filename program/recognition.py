import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
import numpy as np
from sewar.full_ref import ssim 
from scipy.spatial.distance import *


scale = 30

#pattern_name = "secretkeeper"
#key_content=["k","p","yo","kfb","k2tog","ssk","cdd","k","k"] 

pattern_name = "wintermute"
key_content= ["T4F","ssk","T3B","C4B","k","yo","T3F","p","CDD","T4B","k1tbl","CO/BO"]
stitch_content = [0,-1,0,0,0,1,0,0,-2,0,0,0,-1]
#T4B->C4B, CDD->yo

#pattern_name = "oceanbound"
#key_content=["k","yo","k2tog","kfbf","cdd","k","k"]
#stitch_content=[0,1,-1,2,-2,0,0]

#pattern_name = "nurmilintu"
#key_content = ["k","k","k","k","p","k","kfb","k","yo","k","k2tog","k","ssk","k","sk2p","k"]
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
        #self.read_chart()
        pass
    def process(self):
        self.read_keys()
        self.split()
        self.traversal()
    def read_keys(self):
        original_keys = cv2.imread('../src/'+pattern_name+'_key.png',cv2.IMREAD_GRAYSCALE)
        keys = find_stats(original_keys,scale)
        if len(keys) == 0:
            return False
        key_count = 0
        for x,y,w,h,area in keys: 
            width = round(w/h)
            if width < 10: #small unwanted slice
                key = Key(key_content[key_count],original_keys[y:y+h,x:x+w],width)
                self.key_list[width].append(key)
                key_count+=1
        return True
        
    def read_chart(self):
        self.original = cv2.imread('./wintermute_cropped.png',cv2.IMREAD_GRAYSCALE)
        #self.original = cv2.imread('./1.png',cv2.IMREAD_GRAYSCALE)
        self.grid = find_stats(self.original,scale)
        if len(self.grid) == 0:
            return False
        self.size = round(np.mean(self.grid[:,3]))
        self.process()
        return True
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
        f=open("../src/"+pattern_name+"_written.txt","r")
        row=1
        for i in range(len(self.pattern)):
            tmp_list=[]
            res=""
            stitch_inc=0
            for j in range(len(self.pattern[i])):
                x,y,w,h,area = self.pattern[i][j]
                g=self.original[y:y+h,x:x+w]         
                content, stitch = self.compare_grid(g)
                stitch_inc+=stitch
                if content!="":
                    tmp_list.append(content) 
            print(stitch_inc)
            if len(tmp_list)>0:
                written = f.readline()[:-1]
                res = str(row)+": "+', '.join(tmp_list)
                print(res)
                row+=1
                ws = written[3:].split(', ')
                """for w in range(len(ws)):
                    if ws[w]!=tmp_list[w]:
                        print(ws[w]+" / "+tmp_list[w])"""
                print(res == written)
                #f.write(res+"\n")   
        f.close()
    def compare_grid(self,grid):
        if grid.shape[0]<0.8*self.size or grid.shape[1]<0.8*self.size:
            return "",0
        if(isBlank(grid)):
            return "k",0
        width = round(grid.shape[1]/grid.shape[0])
        res = self.cmpsim(grid,width)
        return [self.key_list[width][res].abbr, stitch_content[res]]
    def cmpsim(self,grid,width):
        grid = cv2.resize(grid,(self.size*width,self.size))
        key = [self.key_list[width][i].symbol for i in range(len(self.key_list[width]))]
        gmean = np.mean(grid)
        diff =[abs(gmean-np.mean(key[i])) for i in range(len(key))]
        sim=[0 for i in range(len(key))]
        for i in range(len(key)):
            if (not isBlank(key[i])) and key_content[i]!='k' and diff[i]<10:
                sim[i]= self.cos(key[i],grid)
        return np.argmax(sim)
    
    def cos(self,key,grid):
        transpose_grid = grid.transpose()
        transpose_key = key.transpose()
        dist = []
        one = [1 for i in range(grid.shape[1])]
        for i in range(grid.shape[1]):
            dist.append(1-cosine(transpose_grid[i],transpose_key[i]))
        sim_ver = 1-cosine(one,dist)
        return sim_ver
    def setWS(self,flag):
        self.WS = flag

if __name__ == "__main__":
    Transfer()