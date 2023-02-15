import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.color import rgb2gray
from PIL import Image, ImageEnhance

img = cv2.imread('screenshot.png',0)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
scale=2
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(src.shape[1]//scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,src.shape[0]//scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
#table = cv2.bitwise_or(result1,result2)
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


image = cv2.imread('21.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray = 255-gray
gray = 255*(gray < 128).astype(np.uint8)
coords = cv2.findNonZero(gray)
x, y, w, h = cv2.boundingRect(coords)
target= gray[y:y+h,x:x+w]
target = cv2.resize(target,(64,64))
target = (target < 128).astype(np.uint8)
avg = np.mean(target)
thash=[]
for i1 in range(64):
    for j1 in range(64):
        if target[i1,j1] > avg:
            thash.append(1)
        else:
            thash.append(0)

ind=1
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
                #cv2.imwrite(str(ind)+'.png',test)
                avg = np.mean(test)
                hash=[]
                for i1 in range(64):
                    for j1 in range(64):
                        if test[i1,j1] > avg:
                            hash.append(1)
                        else:
                            hash.append(0)
                n=0
                for k in range(len(hash)):
                    if hash[k]!=thash[k]:
                        n+=1
                if 1-n / len(hash)>0.8:
                    print(ind)

        ind+=1
