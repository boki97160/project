import cv2
import numpy as np
from PIL import Image
#import imagehash
#from skimage.metrics import structural_similarity

original=cv2.imread('./src/nurmilintu_key.png')

img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)

scale = 15
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)

ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
stats = stats[2:]
key_number=1
key_list=[]
for x,y,w,h,area in stats: #0,1 = background 
    cv2.imwrite("key"+str(key_number)+'.png',original[y:y+h,x:x+w])
    key_list.append(img[y:y+h,x:x+w])
    key_number+=1


original=cv2.imread('./src/nurmilintu_chart.png')

img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)

scale = 15
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)
cv2.imwrite('table.png',table)
cv2.imwrite('intersect.png',table)

ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
stats = stats[2:]
grid_number=1
grid_list=[]
for x,y,w,h,area in stats: #0,1 = background 
    #cv2.imwrite('grid'+str(grid_number)+'.png',original[y:y+h,x:x+w])
    grid_list.append(img[y:y+h,x:x+w])
    #cv2.imwrite((str(grid_number)+'.png'),grid_list[grid_number-1])
    grid_number+=1

i=0
size=12
for grid in grid_list[:30]:
    ind=0
    max1=0
    for k in range(len(key_list)):
        grid = cv2.resize(grid,(size,size))
        key_list[k]=cv2.resize(key_list[k],(size,size))
        ssim= structural_similarity(grid,key_list[k])
        if ssim>max1:
            max1=ssim
            ind=k
            print(i,ind,max1)
    #cv2.imwrite(str(i)+"-1.png",key_list[ind])
    #cv2.imwrite(str(i)+"-2.png",grid)
    i+=1

"""
size=20
key_hash=[]

for key in key_list:
    key = cv2.resize(key,(size,size))
    avg = np.mean(key)
    hash=[]
    for i1 in range(size):
        for j1 in range(size):
            if key[i1,j1] < avg:
                hash.append(1)
            else:
                hash.append(0)
    key_hash.append(hash)

i=1
for grid in grid_list[:50]:
    image_one_hash = imagehash.average_hash(Image.open('grid'+str(i)+'.png'))
    """
"""
    grid = cv2.resize(grid,(size,size))
    avg = np.mean(grid)
    hash=[]
    for i1 in range(size):
        for j1 in range(size):
            if grid[i1,j1] < avg:
                hash.append(1)
            else:
                hash.append(0)
    #max=0
    min=9999
    ind=0
    for k in range(len(key_list)):
        n=0
        for l in range(len(key_hash[k])):
            if hash[l] != key_hash[k][l]:
                n+=1
        if n<min:
            ind=k
            #max=1-n/((size**2))
            min=n
            print(i,ind,n,min)
    #cv2.imwrite(str(i)+"-1.png",key_list[ind])
    #cv2.imwrite(str(i)+"-2.png",grid)
    """"""
    max =0
    maxsim=99999
    for k in range(1,9):
        image_two_hash=imagehash.average_hash(Image.open('key'+str(k)+'.png'))
        sim=image_one_hash-image_two_hash
        if sim<maxsim:
            maxsim=sim
            ind = k
            print(i,ind,1-(sim/size**2))
    
    i+=1
"""