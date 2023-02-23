import cv2
from sewar.full_ref import ssim

img1 = cv2.imread('./src/ssk.png',0)
img2 = cv2.rotate(img1,cv2.ROTATE_90_CLOCKWISE)

i1=cv2.resize(img1,(45,45),interpolation=cv2.INTER_AREA)
i2=cv2.resize(img2,(45,45),interpolation=cv2.INTER_AREA)
print(ssim(i1,i2))