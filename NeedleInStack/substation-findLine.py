__author__ = 'zhengyiwang'

import cv2
import numpy as np

img = cv2.imread("findLine-substation-3.png")

# cv2.imshow('test-hsv.jpg', np.hstack((cv2.Canny(equ, 500, 1000), cv2.Canny(equ, 300, 500), cv2.Canny(equ, 300, 1000), cv2.Canny(equ, 900, 1000))))

edges = cv2.Canny(img, 100, 500)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, minLineLength=400, maxLineGap=30)
# lines = cv2.HoughLines(edges, 1, np.pi/180, 175)

for line in lines:
    line = line.ravel()
    cv2.line(img, tuple(line[0:2]), tuple(line[2:4]), (0, 0, 255), 2)
    continue
    for rho, theta in line:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*a)
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*a)

        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)

cv2.imshow('Result', np.hstack((img, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))))
cv2.imwrite('findLine-lines-3.jpg', img)
cv2.imwrite('findLine-edges-3.jpg', edges)
cv2.waitKey()
