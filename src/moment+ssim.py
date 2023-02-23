
from sewar.full_ref import ssim
from scipy.spatial import distance as dist
import numpy as np
import mahotas
import cv2
import imutils

scale = 30
key_list=[]
key_content=["k","yo","k2tog","kfbf","cdd","k"]

def find_stats(original, scale):
    img = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
    ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
    result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
    result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    table = cv2.bitwise_or(result1,result2)
    ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
    stats = stats[2:]
    return stats


def compare_grid(grid):
    mind = []
    pos = []
    sim = []
    size = min(grid.shape[0],grid.shape[1])
    if size%2==0:
        size-=1
    grid= cv2.resize(grid,(size,size),interpolation=cv2.INTER_AREA)
    for k in range(len(key_list)):
        key=cv2.resize(key_list[k],(size,size),interpolation=cv2.INTER_AREA)
        fk = zernike(key)
        fg = zernike(grid)
        d = np.linalg.norm(fk - fg)
        if len(mind) < 2:
            mind.append(d)
            pos.append(k)
            score,_ = ssim(key,grid)
            sim.append(score)
        elif d < max(mind):
            arg = np.argmax(mind)
            mind[arg] = d 
            pos[arg] = k 
            score,_ = ssim(key,grid)
            sim[arg]=score
    return pos[np.argmax(sim)]

def zernike(img): 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    gray = 255-gray
    features = mahotas.features.zernike_moments(gray,min(img.shape[0],img.shape[1])/2,degree=8)
    return features

original = cv2.imread('./src/oceanbound_key.png')
key = find_stats(original,scale)

i=1
for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    key_list.append(block)
    cv2.imwrite(str(i)+'.png',block)
    i+=1

original = cv2.imread('./src/oceanbound_chart.png')
grid = find_stats(original,scale)

dist = 12
last_y=-1

list=[]
infor=[]


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

pattern=[]
for i in range(len(infor)):
    list=[]
    for j in range(len(infor[i])):
        x,y,w,h,area = infor[i][j]
        g=original[y:y+h,x:x+w]
        content = key_content[compare_grid(g)]
        list.append(content)
    print(list)
