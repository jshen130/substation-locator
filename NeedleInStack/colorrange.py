__author__ = 'zhengyiwang'

import cv2
import numpy as np
import math


img = cv2.imread()
img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

green= cv2.inRange(img_HSV, np.array([0, 0, 120], np.uint8), np.array([180, 100, 255], np.uint8))
