import pyzbar.pyzbar as pyzbar
import cv2

img = cv2.imread('E:/yzm/20200514105106_1.png')
barcodes = pyzbar.decode(img)
# for barcode in barcodes:
#     print(barcode.rect)
#     x, y, w, h = barcode.rect
#     print(x+w,y+h)
print(len(barcodes))