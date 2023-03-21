from sewar.full_ref import ssim
import cv2


img1 = cv2.imread('./src/kfbf.png')
img2 = cv2.imread('./src/yo.png')
img2 = cv2.resize(img2,(img1.shape[1],img1.shape[0]))

print(ssim(img1,img2))