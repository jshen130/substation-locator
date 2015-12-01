__author__ = 'zhengyiwang'

import cv2
import numpy as np
import datetime

print "Start: " + str(datetime.datetime.now())

img = cv2.imread("findLine-substation-3.png")
img = cv2.imread("../training-images/substation_31/" + "substation_31_img1_y38.191553_x-120.82906_z20" + ".png")

#edges = cv2.Canny(img, 100, 500)
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#print "Mean HSV: " + str(cv2.mean(img_HSV))
if cv2.mean(img_HSV)[2] < 100:
    edges = cv2.inRange(img_HSV, np.array([0, 0, 120], np.uint8), np.array ([180, 100, 255], np.uint8))
else:
    edges = cv2.inRange(img_HSV, np.array([0, 0, 0], np.uint8), np.array ([180, 255, 100], np.uint8))
    edges = cv2.inRange(img_HSV, np.array([0, 0, 160], np.uint8), np.array ([180, 25, 255], np.uint8))

print "Edges detected: " + str(datetime.datetime.now())

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, minLineLength=250, maxLineGap=30)
# lines = cv2.HoughLines(edges, 1, np.pi/180, 175)

print "Lines detected: " + str(datetime.datetime.now())

if lines is not None:
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

print "End: " + str(datetime.datetime.now())

cv2.imshow('Result', np.hstack((img, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))))
cv2.imwrite('findLine-lines-3.jpg', img)
cv2.imwrite('findLine-edges-3.jpg', edges)
cv2.waitKey(10000)
