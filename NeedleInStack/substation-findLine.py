__author__ = 'zhengyiwang'

import cv2
import numpy as np
import datetime
import math
import matplotlib.pyplot as plt
plt.ion()

print "Start: " + str(datetime.datetime.now())

img = cv2.imread("findLine-substation-3.png")
img = cv2.imread("../training-images/substation_31/" + "substation_3_img72_y44.7725058_x-122.6746753_z20" + ".png")
img = cv2.imread("../training-pos/" + "substation_18_img49_y37.22573_x-121.74645_z20" + ".png")

#edges = cv2.Canny(img, 100, 500)
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#print "Mean HSV: " + str(cv2.mean(img_HSV))
if cv2.mean(img_HSV)[2] < 100:
    edges = cv2.inRange(img_HSV, np.array([0, 0, 120], np.uint8), np.array([180, 100, 255], np.uint8))
else:
    edges = cv2.inRange(img_HSV, np.array([0, 0, 0], np.uint8), np.array([180, 255, 100], np.uint8))
    # edges = cv2.inRange(img_HSV, np.array([0, 0, 160], np.uint8), np.array([180, 25, 255], np.uint8))

edges = cv2.Canny(edges, 100, 500)
print "Edges detected: " + str(datetime.datetime.now())

lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, minLineLength=250, maxLineGap=30)
# lines = cv2.HoughLines(edges, 1, np.pi/180, 175)

print "Lines detected: " + str(datetime.datetime.now())

if lines is None:
    print "NO LINES DETECTED!"
else:
    theta = np.empty(len(lines))
    d = np.empty(len(lines))
    cnt = 0
    for line in lines:
        line = line.ravel()
        theta[cnt] = (math.pi/2 - math.atan2(line[1]-line[3], line[2]-line[0])) % math.pi
        d[cnt] = line[2]*math.cos(theta[cnt]) + line[3]*math.sin(theta[cnt])
        print "Line detected: " + str(tuple(line[0:2])) + "; " + str(tuple(line[2:4])) + "\t->\tth=" + str(math.degrees(theta[cnt])) + ", d=" + str(d[cnt])
        cnt += 1
        cv2.line(img, tuple(line[0:2]), tuple(line[2:4]), (0, 0, 255), 2)

        # cv2.imshow('Result', np.hstack((img, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))))
        # plt.hist2d([math.degrees(t) for t in theta], d, bins=30, range=np.array([[0, 180], [0, 700]]))
        # if cnt == 1: plt.colorbar()
        # cv2.waitKey(1000)

    plt.figure()
    plt.hist2d([math.degrees((-t+math.pi/2) % math.pi) for t in theta], d, bins=30, range=np.array([[0, 180], [-600, 700]]))
    plt.colorbar()

    plt.figure()
    plt.hist([math.degrees((-t+math.pi/2) % math.pi) for t in theta], bins=30, range=np.array([0, 180]))


print "End: " + str(datetime.datetime.now())

cv2.imshow('Result', np.hstack((img, cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB))))
# cv2.imwrite('findLine-lines-3.jpg', img)
# cv2.imwrite('findLine-edges-3.jpg', edges)
cv2.waitKey(0)
