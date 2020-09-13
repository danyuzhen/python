# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 20:00:21 2019

@author: admin
"""

import cv2
import numpy as np

img=cv2.imread('trip.png')
img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gradx = cv2.Sobel(img, ddepth =cv2.CV_32F, dx =1,  dy = 0,ksize = -1)
grady = cv2.Sobel(img, cv2.CV_32F, 0, 1,-1)

#过滤得到的X方向像素值减去Y方向的像素值：
gradient = cv2.subtract(gradx, grady)
gradient = cv2.convertScaleAbs(gradient)

#缩放元素再取绝对值，最后转换格式为8bit型
blurred = cv2.blur(gradient, (9, 9))
(_, thresh) = cv2.threshold(blurred, 160, 160, cv2.THRESH_BINARY)

#均值滤波取二值化
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

#腐蚀和膨胀的函数
closed = cv2.erode(closed, None, iterations = 4)
closed = cv2.dilate(closed, None, iterations = 4)

#找到边界findContours函数
binary,cnts,hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

#计算出包围目标的最小矩形区域：
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
rect = cv2.minAreaRect(c)
box = np.int0(cv2.boxPoints(rect))

img1=img[477:577,300:777]
cv2.imshow("hui",closed)
cv2.waitKey(0)
cv2.destroyAllWindows()