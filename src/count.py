import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from PIL import Image, ImageEnhance

img = cv2.imread('screenshot6.png',0)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
#scale
#scale=10sc.shape[1]//scale
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(15,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,15))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)
cv2.imwrite('intersect1.png',intersect)
cv2.imwrite('table1.png',table)
pos = np.where(intersect == 255)

p1 = []
last = 0
for i in pos[0]:
    if i !=last+1 and i not in p1:
        p1.append(i)
    last=i

p2 = []
last = 0
for j in pos[1]:
    if j != last+1 and j not in p2:
        p2.append(j)
    last = j
list =[]
thl =[]
ind=1
first = True
for i in range(len(p1)-1):
    for j in range(len(p2)-1):
        gray = src[p1[i]:p1[i+1],p2[j]:p2[j+1]]
        gray = 255-gray
        coords = cv2.findNonZero(gray)
        x1,y1,x2,y2 = cv2.boundingRect(coords)
        test = gray[y1:y2,x1:x2]
        if test.size>0 :
            test = cv2.resize(test,(64,64))
            test = 255*(test < 128).astype(np.uint8)
            if test.any():
                avg = np.mean(test)
                hash=[]
                for i1 in range(64):
                    for j1 in range(64):
                        if test[i1,j1] > avg:
                            hash.append(1)
                        else:
                            hash.append(0)

                if first == True:
                    thl.append(hash)
                    list.append(test)
                    first = False
                else:
                    found = False
                    l=0
                    for l in range(len(thl)):
                        n=0
                        for k in range(len(thl[l])):
                            if hash[k] != thl[l][k]:
                                n+=1
                        thresh = 0.98
                        if 1- n / len(hash) > thresh:
                            found=True
                            break
                    if found == False:
                        thl.append(hash)
                        list.append(test)
                        #cv2.imwrite(str(ind)+'.png',test)

        ind+=1
