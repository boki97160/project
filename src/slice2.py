import cv2
import numpy as np

img = cv2.imread('screenshot4.png',0)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)
scale = 5
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(src.shape[1]//scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,src.shape[0]//scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)
cv2.imwrite("intersect.png",intersect)
cv2.imwrite("table.png",table)

py, px = np.where(table==255)

x=[]
y=[]

for i in range(1,len(px)):
    if px[i]-px[i-1] >1 and py[i]-py[i-1]>1 :
        x.append(px[i])
        y.append(py[i])

print(len(px))
"""
py, px = np.where(intersect == 255)

x=[]
y=[]
for i in range(len(px)-1):
    if px[i+1]-px[i] > 1 or py[i+1]-py[i] > 1:
        x.append(px[i])
        y.append(py[i])
x.append(px[len(px)-1])
y.append(py[len(py)-1])
"""