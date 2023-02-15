import cv2
import numpy as np

img = cv2.imread('penguin.jpg',0)
ret, img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
cv2.imwrite('original.jpg',img)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel)
cv2.imwrite('ero.jpg',erosion)
dilation = cv2.dilate(img,kernel)
cv2.imwrite('dila.jpg',dilation)
