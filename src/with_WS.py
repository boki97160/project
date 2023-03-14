import cv2
import numpy as np
from sewar.full_ref import ssim#from skimage.metrics import structural_similarity

scale= 30
key_content=["T4F","ssk","T3B","C4B","k","yo","T3F","p","CDD","T4B","k1tbl","CO/BO"]
#key_content=["k","yo","k2tog","kfbf","cdd","k"]
#key_content = ["k","p","yo","kfb","k2tog","ssk","cdd","k","k"]
#key_content=["k","p","k2tog","ssk","yo","cdd","kfb","k"]
key_list=[]
#key_content = ["","k","k","k","p","k","kfb","k","yo","k","k2tog","k","ssk","k","sk2p","k"]

f=open("./src/wintermute_written.txt","r")
def find_stats(original, scale):
    img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
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
    ind=0
    max1=0
    size = min(grid.shape[0],grid.shape[1])
    if size%2==0:
        size-=1
    grid = cv2.resize(grid,(size,size),interpolation=cv2.INTER_AREA)
    for k in range(len(key_list)):
        key=cv2.resize(key_list[k],(size,size),interpolation=cv2.INTER_AREA)
        sim, _= ssim(grid,key)
        if sim>max1:
            max1=sim
            ind=k
    return ind

def print_instruction(row):
    j=1
    end_str=', '
    for i in range(len(row)-1):
        if i== len(row)-2:
            end_str='\n'
        if row[i] == row[i+1] and (row[i]=='k' or row[i]=='p'):
            j+=1
        else:
            if row[i]=='k' or row[i]=='p':
                print(row[i]+str(j),end=end_str)
                j=1
            else:
                print(row[i],end=end_str)

original = cv2.imread('./src/wintermute_key.png')
key = find_stats(original,scale)
key_list = []

i=1
for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    key_list.append(block)
    i+=1

original = cv2.imread('./src/wintermute_chart.png')
grid = find_stats(original,scale)

dist = 12
last_y=-1

list=[]
infor=[]



print("with ws? (y/n)")
s = input()


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
        """if (i+1)%2 == 0 and s=="y":
            if content == "p":
                content = "k"
            elif  content == "k":
                content = "p"""
        list.append(content)
    """if s == "y" and (i+1)%2 ==0:
        list.reverse()"""
    list.append(" ")
    row=0
    if  s=="y":
        print("row"+str(i+1)+":",end=" ")
        row=i+1
    else:
        print("row"+str(2*i+1)+": ", end=" ")
        row=2*i+1
    print_instruction(list)
    if len(list)>0:
        written = f.readline()[:-1]
        row+=1
        ws = written[3:].split(', ')
        for w in range(len(ws)):
            if ws[w]!=list[w]:
                print(ws[w]+" / "+list[w])
    #print_instruction(list)