import cv2
import numpy as np
import datetime

def colorCube(img_HSV):
    n_h = 2
    n_s = 2
    n_v = 2
    Hlower = 0
    Slower = 0
    Vlower = 0
    HCubelength = 180 / n_h
    SCubelength = 255 / n_s
    VCubelength = 255 / n_v
    CubeCountColor = []
    for h in range(n_h):
        Slower = 0
        for s in range(n_s):
            Vlower = 0
            for v in range(n_v):
                Hhigher = Hlower + HCubelength
                Shigher = Slower + SCubelength
                VHigher = Vlower + VCubelength
                result = cv2.inRange(img_HSV, np.array([Hlower, Slower, Vlower], np.uint8), np.array ([Hhigher, Shigher, VHigher], np.uint8))
                count = cv2.countNonZero(result)
                CubeCountColor.append(count)
                Vlower = VHigher
            Slower = Shigher
        Hlower = Hhigher

    return CubeCountColor

def meanHSV(img_HSV):
    return cv2.mean(img_HSV)

if __name__ == "__main__":
    img = cv2.imread("findLine-substation-2.png")
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print colorCube(img_HSV)