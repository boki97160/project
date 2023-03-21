from sewar.full_ref import ssim
import numpy as np
import mahotas
import cv2
from scipy.spatial.distance import directed_hausdorff
import math
import heapq

first = True
project_name = "oceanbound"
#f=open("./src/"+project_name+"_written.txt","w+")
f=open("./src/"+project_name+"_written.txt","r")
size = 1000
scale = 30
key_list=[]
key_zernike=[]
keys=[[] for i in range(10)]
#secretkeeper
#key_content=["k","p","yo","kfb","k2tog","ssk","cdd","k","k"] 

#wintermute
#key_content= ["T4F","ssk","T3B","C4B","k","yo","T3F","p","CDD","T4B","k1tbl","CO/BO"]
#oceanbound
key_content=["k","yo","k2tog","kfbf","cdd","k","k"]
#nurmilintu
#key_content = ["","k","k","k","p","k","kfb","k","yo","k","k2tog","k","ssk","k","sk2p","k"]

def addbg(target,width):
    bg_size = size * math.ceil(1.5*width)
    w,h = target.shape[1],target.shape[0]
    image = np.zeros((bg_size,bg_size),dtype="uint8")
    overlay = np.zeros((bg_size,bg_size),dtype="uint8")
    hsize = bg_size//2
    overlay[hsize-h//2:hsize-h//2+h,hsize-w//2:hsize-w//2+w] = 255-target
    cv2.addWeighted(src1=image, alpha=1, src2=overlay, beta=1.0, gamma=0, dst=image)
    return 255-image

def find_stats(original, scale):
    #img = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    src= cv2.threshold(original,250,255,cv2.THRESH_BINARY_INV)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
    result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
    result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    table = cv2.bitwise_or(result1,result2)
    stats= cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)[2][2:]
    return stats


def check_blank(grid):
    c=0
    #grid = cv2.cvtColor(grid,cv2.COLOR_BGR2GRAY)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j]>=250):
                c+=1
    return( c>grid.shape[0]*grid.shape[1]*0.95)

def cmpsim(grid,width):
    sim =[]
    grid = cv2.resize(grid,(size*width,size))
    """"""
    global first
    if first == True:
        np.savetxt('test.txt',grid,fmt="%d")
        first = False
    """"""
    fg = zernike(addbg(grid,width))
    for key in keys[width]:
        fk = key['moments']
        sim.append({'abbr':key['abbr'],'dist':np.linalg.norm(fk - fg),'ssim':ssim(key['symbol'],grid)})
    #sim.sort(key = lambda x : x[1])
    smallest = heapq.nsmallest(4,sim,key=lambda x:x['dist'])
    #smallest.sort(key = lambda x : x['ssim'], reverse=True)
    smallest.sort(key = lambda x : x['ssim'], reverse = True)
    return smallest[0]['abbr']

def compare_grid(grid):
    if grid.shape[0]<0.8*size or grid.shape[1]<0.8*size:
        return ""
    
    if(check_blank(grid)):
        return "k"
    width = round(grid.shape[1]/grid.shape[0])
    return cmpsim(grid,width)

def zernike(img):
    thresh = cv2.threshold(255-img, 50, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, 1, 2)[0]
    minx,miny = img.shape[0],img.shape[1]
    maxx,maxy = 0,0
    for cnt in contours:        
        x, y, w, h = cv2.boundingRect(cnt)
        minx = min(x,minx)
        miny = min(y,miny)
        maxx = max(x+w,maxx)
        maxy = max(y+h, maxy)
    x,y,w,h = minx,miny,maxx-minx,maxy-miny
    radius = math.ceil(math.hypot(w,h)/2)
    center = (round(x+w/2),round(y+h/2))
    rect = img[center[1]-radius:center[1]+radius,center[0]-radius:center[0]+radius]
    features = mahotas.features.zernike_moments(rect,radius,degree=8)
    return features

original = cv2.imread('./src/'+project_name+'_key.png',0)
key = find_stats(original,scale)

for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    key_list.append(block)
    

original = cv2.imread('./src/'+project_name+'_chart.png',0)
grid = find_stats(original,scale)
dist = 12
last_y=-1

list=[]
infor=[]


size=round(np.mean(grid[:,3]))

for k in range(len(key_list)):
    key = key_list[k]
    width = round(key.shape[1]/key.shape[0])
    if width>10:
        continue
    if check_blank(key):
        keys[width].append({'abbr':key_content[k],'symbol':cv2.resize(key,(size*width,size)),'moments':1e7})
    else:
        
        keys[width].append({'abbr':key_content[k],'symbol':cv2.resize(key,(size*width,size)),'moments':zernike(addbg(key,width))})

for now in grid:
    x,y,w,h,area = now
    if(abs(y-last_y)>dist):
        last_y=y
        list.sort(reverse=True,key=lambda x:(x[0]))
        infor.append(list)
        list=[]
    list.append(now)

list.sort(reverse=True,key=lambda x:(x[0]))
infor.append(list)
infor = infor[::-1]

row=1
pattern=[]
for i in range(len(infor)):
    list=[]
    res=""
    img1 = original.copy()
    for j in range(len(infor[i])):
        x,y,w,h,area = infor[i][j]
        g=original[y:y+h,x:x+w]            
        content = compare_grid(g)
        if content!="":
            list.append(content)  
    if len(list)>0:
        written = f.readline()[:-1]
        res = str(row)+": "+', '.join(list)
        print(res)
        row+=1
        ws = written[3:].split(', ')
        for w in range(len(ws)):
            if ws[w]!=list[w]:
                print(ws[w]+" / "+list[w])
        print(res == written)
        #f.write(res+"\n")   
f.close()