import cv2
import numpy as np

img = cv2.imread('./src/oceanbound_chart.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#gray = 255-gray
gray = 255*(gray < 128).astype(np.uint8)
coords = cv2.findNonZero(gray)
x, y, w, h = cv2.boundingRect(coords)
rect = img[y:y+h,x:x+w]
cv2.imwrite("cropped1.png", rect)
