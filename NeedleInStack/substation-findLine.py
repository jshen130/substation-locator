__author__ = 'zhengyiwang'
__author__ = 'zhengyiwang'
import cv2

import numpy as np

img = cv2.imread("Substation_example.png")
gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
equ = cv2.equalizeHist(gray)

res = np.hstack((gray,equ)) #stacking images side-by-side
cv2.imwrite('res.png',res)

edges = cv2.Canny(equ,200,550,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,230)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)


cv2.imwrite('imgWithLine.jpg',img)

cv2.imwrite('edge.jpg',edges)
