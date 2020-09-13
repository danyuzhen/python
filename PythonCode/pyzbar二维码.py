import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from scipy import ndimage

img_filename = "C:\\Users\\Administrator\\Desktop\\yzm\\img1.png"
img = cv2.imread(img_filename)

kernel_3x3=np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
kernel_5x5=np.array([[-1,1,2,1,-1],[-1,2,4,2,-1],[-1,1,2,1,-1],[-1,-1,-1,-1,-1]])
img=cv2.imread(img_filename,0)
k3=ndimage.convolve(img,kernel_3x3)
k5=ndimage.convolve(img,kernel_5x5)
blurred=cv2.GaussianBlur(img,(17,17),0)

barcodes = pyzbar.decode(img)
for barcode in barcodes:
    x, y, w, h = barcode.rect
print(x, y, w, h)
barcodes1 = pyzbar.decode(k5)
for barcode in barcodes1:
    x, y, w, h = barcode.rect

print(x, y, w, h)
cv2.imshow("im", img[y:y + h, x:x + w])
cv2.imshow("im1", k5)
cv2.waitKey(10000)
cv2.destroyAllWindows()