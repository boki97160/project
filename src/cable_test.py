import cv2
import numpy as np
from skimage.metrics import structural_similarity

original=cv2.imread('nurmilintu_key.png')

img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)

scale = 30
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
    key_list.append(original[y:y+h,x:x+w])
    cv2.rectangle(original,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imwrite(str(key_number)+'.png',original[y:y+h,x:x+w])
    key_number+=1

cv2.imwrite('original.png',original)
original=cv2.imread('nurmilintu_chart.png')

img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)

scale = 30
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)


ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
stats = stats[2:]
grid_number=1
grid_list=[]
for x,y,w,h,area in stats: #0,1 = background 
    #cv2.rectangle(original,(x,y),(x+w,y+h),(0,255,0),2)
    #cv2.imwrite(str(grid_number)+'.png',original[y:y+h,x:x+w])
    #grid_list.append(img[y:y+h,x:x+w])
    grid_list.append(original[y:y+h,x:x+w])
    #cv2.imwrite((str(grid_number)+'.png'),grid_list[grid_number-1])
    grid_number+=1
#cv2.imwrite('original.png',original)
i=0
size=36
for grid in grid_list:
    ind=0
    max1=0
    for k in range(len(key_list)):
        grid = cv2.resize(grid,(size,size))
        key_list[k]=cv2.resize(key_list[k],(size,size))
        ssim= structural_similarity(grid,key_list[k],multichannel=True)
        if ssim>max1:
            max1=ssim
            ind=k
            print(i,ind,max1)
    #cv2.imwrite(str(i)+"_result.png",key_list[ind])
    #cv2.imwrite(str(i)+"_grid.png",grid)
    i+=1
