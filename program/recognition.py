import cv2
import numpy as np
from scipy.spatial.distance import *
import reader
import pathlib
import subprocess
import sys
import json
scale = 30

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
    key_width = []
    key_img = []
    written_pattern = []
    
    def __init__(self):
        pass
    def process(self,app,ws):
        self.WS = ws
        self.reader = reader.Reader()
        if self.read_chart() == False:
            print("chart")
            self.reader.data_empty(app)
            return
        self.rec = {}
        if self.read_keys(app) == False:
            print("key")
            self.reader.data_empty(app)
            return
        
        subprocess.call([sys.executable,"input_form.py"])
        self.read_key_content()
        self.split()
        if self.traversal() == False or len(self.written_pattern)==0:    
            print("traversal")
            self.reader.data_empty(app)
            return
        json_file = open("./chart.json","w+")
        data = {"pattern":self.written_pattern,"WS":self.WS}
        json.dump(data,json_file)
        json_file.close()
        json_file = open("./pos.json","w+")
        print(type(self.rec["k"]))
        json.dump(self.rec,json_file)
        json_file.close()
        self.reader.getdata()
        self.reader.initUI(app)
    def read_key_content(self):
        self.rec["k"] = []
        
        json_file = open("./key_content.json","r+")
        self.data = json.load(json_file)
        self.key_content = self.data['abbr']
        self.stitch_content = self.data['sts']
        for i in range(len(self.key_content)-1):
            self.rec[self.key_content[i]] = []
            self.stitch_content[i] = int(self.stitch_content[i])
            key = Key(self.key_content[i],self.key_img[i],self.key_width[i])
            self.key_list[self.key_width[i]].append(key)
        json_file.close()
        return True

    def read_keys(self,app):
        
        
        path = pathlib.Path("./key.png")
        if not path.exists():
            return False
        
        original_keys = cv2.imread('./key.png',cv2.IMREAD_GRAYSCALE)
        keys = find_stats(original_keys,scale)
        self.key_count = 0
        for x,y,w,h,area in keys: 
            width = round(w/h)
            if width < 10 and width>=1 and w>15 and h>15: #small unwanted slice
                self.key_img.append(original_keys[y:y+h,x:x+w])
                self.key_width.append(width)
                cv2.imwrite(str(self.key_count)+'.png',original_keys[y:y+h,x:x+w])
                self.key_count+=1
        json_file = open("./key_content.json","w+")
        self.data = {}
        self.data["width"]=self.key_width
        self.data["key_count"] = self.key_count

        json.dump(self.data,json_file)
        json_file.close()
        return True
        
    def read_chart(self):
        path = pathlib.Path("./chart-1.png")
        if not path.exists():
            return False
        self.original = cv2.imread('./chart-1.png',cv2.IMREAD_GRAYSCALE)
        self.grid = find_stats(self.original,scale)
        if len(self.grid) == 0:
            return False
        self.size = round(np.mean(self.grid[:,3]))
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
        #f=open("../src/"+pattern_name+"_written.txt","r")
        for i in range(len(self.pattern)):
            kcount = 0
            pcount = 0
            tmp_list = []
            res=""
            stitch_inc=0
            for j in range(len(self.pattern[i])):
                x,y,w,h,area = self.pattern[i][j]
                g=self.original[y:y+h,x:x+w]         
                content, stitch = self.compare_grid(g)
                if content == "error":
                    continue
                if content!="":
                    self.rec[content].append([int(x),int(y),int(x+w),int(y+h)])
                    stitch_inc+=stitch
                    flag = False
                    if content == "k":
                        kcount+=1;
                    elif content != "k" and kcount!=0:
                        tmp_list.append("k"+str(kcount))
                        kcount=0
                        if content != "p":
                            tmp_list.append(content)
                            flag = True
                    if content == "p":
                        pcount+=1
                    elif content !="p" and pcount!=0:
                        tmp_list.append("p"+str(pcount))
                        pcount=0
                        if content!="k":
                            tmp_list.append(content)
                            flag = True
                    if content !="p" and content!="k" and flag ==False:
                        tmp_list.append(content) 
            #print(stitch_inc)
            if kcount!=0:
                tmp_list.append("k"+str(kcount))
            if pcount!=0:
                tmp_list.append("p"+str(pcount))
            if len(tmp_list)>0:
                #written = f.readline()[:-1]
                res = ', '.join(tmp_list)
                
                #print(res)
                #ws = written[3:].split(', ')
                """for w in range(min(len(ws),len(res))):
                    if ws[w]!=tmp_list[w]:
                        print(ws[w]+" / "+tmp_list[w])"""
                self.written_pattern.append(res)
                #print(res == written)
                #f.write(res+"\n")   
        #f.close()
        return True
    def compare_grid(self,grid):
        if grid.shape[0]<0.8*self.size or grid.shape[1]<0.8*self.size:
            return "",0
        if(isBlank(grid)):
            return "k",0
        width = round(grid.shape[1]/grid.shape[0])
        res = self.cmpsim(grid,width)
        if res == -1:
            return "error",0
        return [self.key_list[width][res].abbr, self.stitch_content[res]]
    def cmpsim(self,grid,width):
        grid = cv2.resize(grid,(self.size*width,self.size))
        key = [self.key_list[width][i].symbol for i in range(len(self.key_list[width]))]
        if len(key)==0:
            return -1
        gmean = np.mean(grid)
        diff =[abs(gmean-np.mean(key[i])) for i in range(len(key))]
        sim=[-1e7 for i in range(len(key))]
        for i in range(len(key)):
            if (not isBlank(key[i])) and self.key_content[i]!='k' and diff[i]<10:
                sim[i]= self.cos(key[i],grid)
                """cv2.imshow('key',key[i])
                cv2.imshow('grid',grid)
                cv2.waitKey(0)
                cv2.destroyAllWindows()"""

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

if __name__ == "__main__":
    Transfer()