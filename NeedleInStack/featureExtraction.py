import cv2
import numpy as np
import math

def colorCube(img_HSV):
    return np.histogramdd(img_HSV.reshape((-1, 3)), bins=[4, 4, 4])[0].ravel().astype(int)

    # n_h = 2
    # n_s = 2
    # n_v = 2
    # Hlower = 0
    # Slower = 0
    # Vlower = 0
    # HCubelength = 180 / n_h
    # SCubelength = 255 / n_s
    # VCubelength = 255 / n_v
    # CubeCountColor = []
    # for h in range(n_h):
    #     Slower = 0
    #     for s in range(n_s):
    #         Vlower = 0
    #         for v in range(n_v):
    #             Hhigher = Hlower + HCubelength
    #             Shigher = Slower + SCubelength
    #             VHigher = Vlower + VCubelength
    #             result = cv2.inRange(img_HSV, np.array([Hlower, Slower, Vlower], np.uint8), np.array ([Hhigher, Shigher, VHigher], np.uint8))
    #             count = cv2.countNonZero(result)
    #             CubeCountColor.append(count)
    #             Vlower = VHigher
    #         Slower = Shigher
    #     Hlower = Hhigher
    #
    # return CubeCountColor

def meanHSV(img_HSV):
    return cv2.mean(img_HSV)

def getLineHist(img_HSV):
    nBins = 30

    if meanHSV(img_HSV) < 100:
        edges = cv2.inRange(img_HSV, np.array([0, 0, 120], np.uint8), np.array([180, 100, 255], np.uint8))
    else:
        edges = cv2.inRange(img_HSV, np.array([0, 0, 0], np.uint8), np.array([180, 255, 100], np.uint8))
        # edges = cv2.inRange(img_HSV, np.array([0, 0, 160], np.uint8), np.array([180, 25, 255], np.uint8))
    edges = cv2.Canny(edges, 100, 500)
    # print "Edges detected: " + str(datetime.datetime.now())

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 75, minLineLength=250, maxLineGap=30)
    # print "Lines detected: " + str(datetime.datetime.now())

    if lines is None:
        #print "NO LINES DETECTED!"
        return np.zeros(nBins)
    else:
        theta = np.empty(len(lines))
        ##d = np.empty(len(lines))
        cnt = 0
        for line in lines:
            line = line.ravel()
            theta[cnt] = (math.pi/2 - math.atan2(line[1]-line[3], line[2]-line[0])) % math.pi
            ##d[cnt] = line[2]*math.cos(theta[cnt]) + line[3]*math.sin(theta[cnt])
            # print "Line detected: " + str(tuple(line[0:2])) + "; " + str(tuple(line[2:4])) + "\t->\tth=" + str(math.degrees(theta[cnt])) + ", d=" + str(d[cnt])
            cnt += 1

        return (np.histogram([math.degrees((-t+math.pi/2) % math.pi) for t in theta], bins=nBins, range=[0, 180])[0] >= 1).astype(int)

if __name__ == "__main__":
    img = cv2.imread("findLine-substation-2.png")
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print colorCube(img_HSV)