import cv2
import numpy as np

original=cv2.imread('./src/oceanbound_key.png')

img = cv2.cvtColor(original,cv2.COLOR_RGB2GRAY)
ret, src= cv2.threshold(img,250,255,cv2.THRESH_BINARY_INV)

scale = 18
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(scale,1))
result1 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,scale))
result2 = cv2.morphologyEx(src, cv2.MORPH_OPEN, kernel)
intersect = cv2.bitwise_and(result1,result2)
table = cv2.bitwise_or(result1,result2)
cv2.imwrite("i.png",intersect)
cv2.imwrite("t.png",table)

ret,labels,stats,centroids = cv2.connectedComponentsWithStats(~table,connectivity=4,ltype=cv2.CV_32S)
o=original
stats = stats[2:]
i=1
for x,y,w,h,area in stats: #0,1 = background 
    #cv2.rectangle(o,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imwrite(str(i)+'.png',original[y:y+h,x:x+w])
    i+=1

#cv2.imwrite('test.png',o)