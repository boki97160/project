from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp
import cv2

blur = cv2.imread('block3.png')
org = cv2.imread('block5.png')

print("MSE: ", mse(blur,org))
print("RMSE: ", rmse(blur, org))
print("PSNR: ", psnr(blur, org))
print("SSIM: ", ssim(blur, org))
print("UQI: ", uqi(blur, org))
print("MSSSIM: ", msssim(blur, org))
print("ERGAS: ", ergas(blur, org))
print("SCC: ", scc(blur, org))
print("RASE: ", rase(blur, org))
print("SAM: ", sam(blur, org))
print("VIF: ", vifp(blur, org))