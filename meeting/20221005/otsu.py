import cv2

img = cv2.imread('two cat.jpg',0)
cv2.imwrite('original.jpg',img)

ret, src = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imwrite('otsu.jpg',src)
