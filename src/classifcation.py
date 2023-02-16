import scipy
import numpy as np
import mahotas
import cv2
import imutils

scale= 30
#key_content=["T4F","ssk","T3B","C4B","k","yo","T3F","p","CDD","T4B","k1tbl/p1tbl","CO/BO"]
key_content=["k","yo","k2tog","kfbf","cdd","k"]
#key_content = ["k","p","yo","kfb","k2tog","ssk","cdd","k","k"]
#key_content=["k","p","k2tog","ssk","yo","cdd","kfb","k"]
key_list=[]

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
    size = min(grid.shape[0],grid.shape[1])
    grid = cv2.resize(grid,(size,size),interpolation=cv2.INTER_AREA)
    sf = [find_features(grid)]
    kd = []
    for k in range(len(key_list)):
        key=cv2.resize(key_list[k],(size,size),interpolation=cv2.INTER_AREA)
        f= find_features(key)
        kd.append(f)
    d= scipy.spatial.distance.cdist(sf,kd)
    i = np.argmin(d)
    print(d)
    print(i)
    print()
    return i

def find_features(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blurred = cv2.GaussianBlur(gray, (13, 13), 0)
    thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)[1]

    # perform a series of dilations and erosions to close holes
    # in the shapes
    thresh = cv2.dilate(thresh, None, iterations=4)
    thresh = cv2.erode(thresh, None, iterations=2)

    # detect contours in the edge map
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnt = imutils.grab_contours(cnts)[0]
    mask = np.zeros(img.shape[:2], dtype="uint8")
    cv2.drawContours(mask, [cnt], -1, 255, -1)

    # extract the bounding box ROI from the mask
    (x, y, w, h) = cv2.boundingRect(cnt)
    roi = mask[y:y + h, x:x + w]
    features = mahotas.features.zernike_moments(roi, cv2.minEnclosingCircle(cnt)[1], degree=8)  

    return features
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

original = cv2.imread('./src/oceanbound_key.png')
key = find_stats(original,scale)
key_list = []

i=1
for x,y,w,h,area in key:
    block = original[y:y+h,x:x+w]
    key_list.append(block)
    i+=1

original = cv2.imread('./src/oceanbound_chart.png')
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
        if (i+1)%2 == 0 and s=="y":
            if content == "p":
                content = "k"
            elif  content == "k":
                content = "p"
        list.append(content)
    if s == "y" and (i+1)%2 ==0:
        list.reverse()
    list.append(" ")
    if  s=="y":
        print("row"+str(i+1)+":",end=" ")
    else:
        print("row"+str(2*i+1)+": ", end=" ")
    print_instruction(list)