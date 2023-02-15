import cv2
import numpy as np
from skimage.metrics import structural_similarity

scale= 30
#key_content=["T4F","SSK","k","T3B","C4B","yo","p","T3F","cdd","k1tbl","T4B","BO"]
key_content=["k","yo","k2tog","kfbf","cdd"," "," "]
key_list=[]

def find_stats(original, scale):
    img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
    ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
    result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
    result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
    table = cv2.bitwise_or(result1,result2)
    cv2.imwrite("table.png",~table)
    ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
    stats = stats[2:]
    return stats


def compare_grid(grid):
    ind=0
    max1=0
    for k in range(len(key_list)):
        size = 12
        grid = cv2.resize(grid,(size,size),interpolation=cv2.INTER_AREA)
        key_list[k]=cv2.resize(key_list[k],(size,size),interpolation=cv2.INTER_AREA)
        ssim= structural_similarity(grid,key_list[k],multichannel=True)
        if ssim>max1:
            max1=ssim
            ind=k
    return ind

def print_instruction(row):
    j=1
    end_str=', '
    for i in range(len(row)-1):
        if i== len(row)-2:
            end_str='\n'
        if row[i] == row[i+1]:
            j+=1
        else:
            if row[i]=='k' or row[i]=='p':
                print(row[i]+str(j),end=end_str)
                j=1
            else:
                print(row[i],end=end_str)

original = cv2.imread('s12.png')
key = find_stats(original,scale)
key_list = []

i=1
for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    i+=1
    key_list.append(block)

original = cv2.imread('screenshot10.png')
grid = find_stats(original,scale)
dist = 8
last_y=-1
list=[]
infor=[]
for now in grid:
    x,y,w,h,area = now
    g=original[y:y+h,x:x+w]
    i+=1
    if(abs(y-last_y)>dist):
        last_y=y
        list.sort(reverse=True,key=lambda x:(x[0]))
        infor.append(list)
        list=[]
    list.append(now)
list.sort(reverse=True,key=lambda x:(x[0]))
infor.append(list)



infor = infor[::-1]
for i in range(len(infor)):
    list=[]
    for j in range(len(infor[i])):
        x,y,w,h,area = infor[i][j]
        g=original[y:y+h,x:x+w]
        list.append(key_content[compare_grid(g)])
    list.append(" ")
    print_instruction(list)

