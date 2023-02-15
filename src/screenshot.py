import numpy as np
import cv2 as cv
drawing = False# true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1

def draw(event,x,y,flags,param):
    global ix,iy,drawing,mode
    if event == cv.EVENT_LBUTTONDOWN:
        drawing=True
        ix,iy = x,y
    elif event == cv.EVENT_MOUSEMOVE:
        if drawing == True:
            img2 = img.copy() 
            cv.rectangle(img2, (ix,iy),(x,y), (0,0,255), 2)
            cv.imshow('image',img2)
    elif event == cv.EVENT_LBUTTONUP:
        drawing = False
        print(ix,iy,x,y)
        cv.imwrite("OAO.png",img[iy:y,ix:x])

img = cv.imread("resized_image3.png")
cv.namedWindow('image')
cv.setMouseCallback('image',draw)
cv.imshow('image',img)
while(1):
    #cv.imshow('image',img)
    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
