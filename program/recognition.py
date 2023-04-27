import cv2
import numpy as np
from scipy.spatial.distance import *
import reader
import pathlib
import subprocess
import sys
import json
from skimage.measure import label as tag
scale = 35


def isBlank(grid):
    if len(grid)==0:
        return True
    src= cv2.threshold(grid,150,255,cv2.THRESH_BINARY_INV)[1]
    return np.mean(src)==0

class Key:
    def __init__(self,abbr,block,width):
        self.abbr = abbr
        self.width = width
        self.symbol = block
        self.cropped = block

class Transfer:
    sum_pattern=0
    size = 0
    pattern = [] 
    key_list = [[] for i in range(20)]
    key_ratio = [[] for i in range(20)]
    key_size = [[] for i in range(20)]
    key_avai = [[] for i in range(20)]
    stitch_content = [[] for i in range(20)]
    stitch_increase = []
    key_width = []
    key_img = []
    written_pattern = []
    k_pos = []
    row_pos=[]
    row_height=[]
    def find_table(self,src):
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
        result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
        result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
        table = cv2.bitwise_or(result1,result2)
        return table
    def find_stats(self,original, source):
        label_num = [0 for i in range(11)]
        table = cv2.threshold(original,255,255,cv2.THRESH_BINARY_INV)[1]
        for i in range(10,0,-1):
            table1 = self.find_table(cv2.threshold(original,25*i,255,cv2.THRESH_BINARY_INV)[1])
            table = table & table1
            num, _ = cv2.connectedComponents(~table)
            if np.sum(table) == 0:
                break
            label_num[i] = num
        table = self.find_table(cv2.threshold(original,25*np.argmax(label_num),255,cv2.THRESH_BINARY_INV)[1])

        if source == "chart":
            labeled,num=tag(table,background=0,return_num=True)
            max_label=0
            max_num=0
            for i in range(1,num+1):
                sub_num = np.sum(labeled==i)
                if sub_num>max_num:
                    max_num=sub_num
                    max_label=i
            if max_label>0:
                table[labeled!=max_label]=0
            stats= cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)[2][1:]
        else:
            
            cv2.imwrite('table.png',table)
            stats= cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)[2][2:]
        return stats
    def __init__(self):
        pass
    def process(self,app,ws,historyname):
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
        print(self.stitch_increase)
        data = {"pattern":self.written_pattern,"WS":self.WS,"increase":self.stitch_increase}
        json.dump(data,json_file)
        json_file.close()
        json_file = open("./pos.json","w+")
        json.dump(self.rec,json_file)
        json_file.close()
        json_file = open("./row_infor.json","w+")
        print(type(self.row_pos),type(self.row_height))
        print(self.row_pos)
        print(self.row_height)
        data = {'row_pos':self.row_pos,'row_height':self.row_height}
        json.dump(data ,json_file)
        json_file.close()
        
        # start read
        self.reader.storehistory(app,historyname)       
        #self.reader.getdata()
        #self.reader.initUI(app)
    def read_key_content(self):
        json_file = open("./key_content.json","r+")
        self.data = json.load(json_file)
        self.key_content = self.data['abbr']
        stitch_content = self.data['sts']
        for i in range(len(self.key_content)):
            self.rec[self.key_content[i]] = []
            
            key = Key(self.key_content[i],self.key_img[i],self.key_width[i])
            self.key_list[self.key_width[i]].append(key)
            self.stitch_content[self.key_width[i]].append(int(stitch_content[i]))
            if self.key_content[i] == "":
                self.key_avai[self.key_width[i]].append(False)
            else:
                self.key_avai[self.key_width[i]].append(True) 
        json_file.close()
        return True

        
    def read_keys(self,app):
        
        path = pathlib.Path("./key.png")
        if not path.exists():
            return False
        
        original_keys = cv2.imread('./key.png',cv2.IMREAD_GRAYSCALE)
        keys = self.find_stats(original_keys,"key")
        self.key_count = 0
        for x,y,w,h,area in keys: 
            width = round(w/h)
            if width < 10 and width>=1 and h>scale*0.9 and w>scale*width*0.9: #small unwanted slice
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
        path = pathlib.Path("./chart.png")
        if not path.exists():
            return False
        self.original = cv2.imread('./chart.png',cv2.IMREAD_GRAYSCALE)
        self.grid = self.find_stats(self.original,"chart")
        if self.grid[0][4] > 10*np.mean(self.grid[:,4]):
            self.grid = self.grid[1:]
        if len(self.grid) == 0:
            return False
        self.size = round(np.mean(self.grid[:,3]))
        return True
    def split(self):
        tmp_list = []
        dist = 12
        
        last_y= self.grid[0][1]
        last_h = self.grid[0][3]
        for now in self.grid:
            x,y,w,h,area = now
            
            if(abs(y-last_y)>dist):
                
                self.row_pos.append(int(last_y))
                self.row_height.append(int(last_h))
                last_y= y
                last_h = h
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
                key = self.key_list[i][j].symbol
                key[key>=127] = 255
                if isBlank(key):
                    self.k_pos.append(j)
                self.key_list[i][j].cropped = self.crop(key)
                self.key_ratio[i].append(self.key_list[i][j].cropped.shape[1]/self.key_list[i][j].cropped.shape[0])
                if self.key_ratio[i][len(self.key_ratio[i])-1]>6:
                    self.key_ratio[i][len(self.key_ratio[i])-1]=6
                self.key_size[i].append(self.key_list[i][j].cropped.shape)
                self.key_list[i][j].cropped = cv2.resize(self.key_list[i][j].cropped,(self.size*self.key_list[i][j].width,self.size))
                """cv2.imshow('key',cv2.resize(self.key_list[i][j].cropped,(150,150)))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                print(self.key_ratio[i][len(self.key_ratio[i])-1])"""
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
                stitch_inc+=stitch
                
                if content == "error":
                    continue
                if content!="":
                    self.sum_pattern+=1
                    self.rec[content].append([int(x),int(y),int(x+w),int(y+h)])
                    
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
            if kcount!=0:
                tmp_list.append("k"+str(kcount))
            if pcount!=0:
                tmp_list.append("p"+str(pcount))
            if len(tmp_list)>0:
                res = ', '.join(tmp_list)
                #print(res)
                self.written_pattern.append(res)
                self.stitch_increase.append(stitch_inc)
                #print(stitch_inc)
        print(self.sum_pattern)

        return True
    def compare_grid(self,grid):
        if grid.shape[0]<0.8*self.size or grid.shape[1]<0.8*self.size:
            return "",0
        
        width = round(grid.shape[1]/grid.shape[0])
        if width > 10:
            return "",0
        res = self.cmpsim(grid,width)
        if res == -1:
            return "error",0
        return [self.key_list[width][res].abbr, self.stitch_content[width][res]]
    def cmpsim(self,grid,width):
        key = [self.key_list[width][i].symbol for i in range(len(self.key_list[width]))]
        mean_diff =[abs(np.mean(grid)-np.mean(key[i])) for i in range(len(key))]

        grid = self.crop(grid)
        if isBlank(grid): # here has problem
            for i in range(len(key)):
                if self.key_avai[width][i] and i in self.k_pos:
                    return i
        
        

        key = [self.key_list[width][i].cropped for i in range(len(self.key_list[width]))]
        avai = [self.key_avai[width][i] for i in range(len(self.key_list[width]))]
        if len(key)==0:
            return -1
        ratio = grid.shape[1]/grid.shape[0]
        if ratio>6:
            ratio = 6
        ratio_diff = [abs(ratio-self.key_ratio[width][i]) for i in range(len(key))]
        
        sim=[-1e7 for i in range(len(key))]
        grid = cv2.resize(grid,(self.size*width,self.size))
        diff = [abs(np.sum(grid<20)-np.sum(key[i]<20))/(self.size*self.size) for i in range(len(key))]

        for i in range(len(key)):
            if mean_diff[i]<20 and diff[i]<0.2 and ratio_diff[i] < 0.2 and avai[i] and not isBlank(key[i]):
                sim[i]= self.cos(key[i],grid)

        if np.max(sim) == -1e7:
            for i in range(len(key)):
                if avai[i] and not isBlank(key[i]):
                    sim[i]= self.cos(key[i],grid)

        """cv2.imshow('grid',cv2.resize(grid,(200,200)))
        cv2.imshow('key',cv2.resize(key[np.argmax(sim)],(200,200)))
        cv2.waitKey(0)
        cv2.destroyAllWindows()"""
        return np.argmax(sim)
    
    def cos(self,key,grid):
        dist = []
        one = [1 for i in range(grid.shape[0])]
        for i in range(grid.shape[0]):
            dist.append(1-cosine(grid[i],key[i]))
        sim_hor = 1-cosine(one,dist)
        transpose_grid = grid.transpose()
        transpose_key = key.transpose()
        dist = []
        one = [1 for i in range(grid.shape[1])]
        for i in range(grid.shape[1]):
            dist.append(1-cosine(transpose_grid[i],transpose_key[i]))
        sim_ver = 1-cosine(one,dist)
        
        return sim_ver**2+sim_hor
    
    def crop(self,rect):
        if not isBlank(rect) and not isBlank(~rect):
            y_nonzero, x_nonzero = np.nonzero(rect<200)
            res = rect[np.min(y_nonzero):np.max(y_nonzero), np.min(x_nonzero):np.max(x_nonzero)]
            if res.shape[0] != 0 and res.shape[1]!=0:
                return res
            else:
                return rect
        else:
            return rect

if __name__ == "__main__":
    Transfer()