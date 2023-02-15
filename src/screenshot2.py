#src https://docs.opencv.org/3.4/db/d5b/tutorial_py_mouse_handling.html
import numpy as np
import cv2
drawing = False# true if mouse is pressed
ix,iy = -1,-1

def draw(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy = x,y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img.copy() 
            cv2.rectangle(img2, (ix,iy),(x,y), (0,0,255), 2)
            cv2.imshow('image',img2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print(ix,iy,x,y)
        times = img3.shape[0]/(297*2)
        iy= int(iy*times)
        y= int(y*times)
        ix= int(ix*times)
        x= int(x*times)
        cv2.imwrite("OAO.png",img3[iy:y,ix:x])

img3 = cv2.imread('src\image3.png')
img = cv2.resize(img3,(210*2,297*2))
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw)
cv2.imshow('image',img)
while(1):
    #cv2.imshow('image',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: #27 == esc
        break
