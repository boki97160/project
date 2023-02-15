import cv2
import numpy as np
import imutils

def main():
    img = cv2.imread('oceanbound_chart.png', 0)   
    # Piece templates:
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)

    pawn_white_template = cv2.imread('block4.png', 0)

    cv2.imshow("Template", pawn_white_template)
    cv2.waitKey(0)

    w_pawn_white, h_pawn_white = pawn_white_template.shape[::-1]

    res_pawn_white = cv2.matchTemplate(img_gray,pawn_white_template,cv2.TM_CCOEFF_NORMED)

    threshhold = 0.6
    loc = np.where(res_pawn_white >= threshhold)

    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_rgb,pt,(pt[0]+w_pawn_white, pt[1]+h_pawn_white),(0,255,255),1)
    cv2.imshow('detected',img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
