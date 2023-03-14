from sewar.full_ref import ssim
import scipy
import numpy as np
import mahotas
import cv2
import imutils
f=open("./src/nurmilintu_written.txt","r")
#f=open("./src/wintermute_written.txt","w+")
m = 10000
scale = 30
key_list=[]
#secretkeeper
#key_content=["k","p","yo","kfb","k2tog","ssk","cdd","k","k"] 

#wintermute
#key_content= ["T4F","ssk","T3B","C4B","k","yo","T3F","p","CDD","T4B","k1tbl","CO/BO"]
#oceanbound
#key_content=["k","yo","k2tog","kfbf","cdd","k","k"]
#nurmilintu
key_content = ["","k","k","k","p","k","kfb","k","yo","k","k2tog","k","ssk","k","sk2p","k"]
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


def count_grid(grid):
    c=0
    grid = cv2.cvtColor(grid,cv2.COLOR_BGR2GRAY)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if(grid[i][j]>=250):
                c+=1
    return( c>grid.shape[0]*grid.shape[1]*0.95)
         

def compare_grid(grid):
    mind = []
    sim = []
    if grid.shape[0]<0.75*m or grid.shape[1]<0.75*m:
        return ""
    pos=[]
    size = min(grid.shape[0],grid.shape[1])
    if size%2==0:
        size-=1
    grid= cv2.resize(grid,(size,size),interpolation=cv2.INTER_AREA)
    
    if(count_grid(grid)):
        return "k"
    for k in range(len(key_list)): 
        if(count_grid(key_list[k])):
            continue   
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
    return key_content[pos[np.argmax(sim)]]

def zernike(img): 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 
    gray = 255-gray
    features = mahotas.features.zernike_moments(gray,min(img.shape[0],img.shape[1])/2,degree=8)
    return features

original = cv2.imread('./src/nurmilintu_key.png')
key = find_stats(original,scale)

i=1
for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    key_list.append(block)
    cv2.imwrite(str(i)+'.png',block)
    i+=1


original = cv2.imread('./src/nurmilintu_chart.png')
grid = find_stats(original,scale)


dist = 12
last_y=-1

list=[]
infor=[]


hmean = []
for now in grid:
    x,y,w,h,area = now
    hmean.append(h)
    if(abs(y-last_y)>dist):
        last_y=y
        list.sort(reverse=True,key=lambda x:(x[0]))
        infor.append(list)
        list=[]
    list.append(now)

m = np.mean(hmean)
list.sort(reverse=True,key=lambda x:(x[0]))
infor.append(list)
infor = infor[::-1]

row=1
pattern=[]
for i in range(len(infor)):
    written = f.readline()[:-1]
    list=[]
    cmp=""
    for j in range(len(infor[i])):
        x,y,w,h,area = infor[i][j]
        g=original[y:y+h,x:x+w]    
        content = compare_grid(g)
        list.append(content)
    cmp+=str(row)+": "
    for l in range(len(list)):
        if(list[l]!=''):
            cmp+=list[l]
            if(l!=len(list)-1):
                cmp+=", "
    print(cmp)
    row+=1
    print(cmp == written)
    #f.write(cmp+"\n")
f.close()