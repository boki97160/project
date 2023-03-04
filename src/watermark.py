import cv2
import numpy as np

size= 500
target = cv2.imread('5.png',0)
w,h = round(target.shape[1]/2),round(target.shape[0]/2)
image = np.zeros((size,size),dtype="uint8")
overlay = np.zeros((size,size),dtype="uint8")
hsize = size//2
overlay[hsize-h:hsize+h,hsize-w:hsize+w] = 255-target

cv2.addWeighted(src1=image, alpha=1, src2=overlay, beta=1.0, gamma=0, dst=image)
cv2.imshow('image',255-image)
cv2.waitKey(0)