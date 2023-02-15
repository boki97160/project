import cv2

img = cv2.imread('two cat.jpg',0)
cv2.imwrite('original.jpg',img)
ret, src = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
cv2.imwrite("bcat.png",src)
ret, src = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
cv2.imwrite("bicat.png",src)
ret, src = cv2.threshold(img,127,255,cv2.THRESH_TRUNC)
cv2.imwrite("tcat.png",src)
ret, src = cv2.threshold(img,127,255,cv2.THRESH_TOZERO)
cv2.imwrite("zcat.png",src)
ret, src = cv2.threshold(img,127,255,cv2.THRESH_TOZERO_INV)
cv2.imwrite("zicat.png",src)
