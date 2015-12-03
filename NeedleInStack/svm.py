__author__ = 'zhengyiwang'
from sklearn import svm
import numpy as np
import cv2
import features1
from sklearn import preprocessing

import os, sys

def allfeatures(img):
    features = []
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #f1 = features1.meanHSV(img_HSV)
    #features += list(f1)
    f2 = features1.colorCube(img_HSV)
    features += list(f2)
    return features

path = os.path.expanduser("~/Workshop/substation-locator/training-pos")
dirs = os.listdir(path)
path2 = os.path.expanduser("~/Workshop/substation-locator/training-neg")
dirs2 = os.listdir(path2)


training = []


totalpositive = 0
for file in dirs[1:-5]:
    totalpositive += 1
    img = cv2.imread(os.path.join(path,file))
    features = allfeatures(img)

    training.append(features)

totalnegative = 0
for file in dirs2[1:-20]:
    totalnegative += 1
    img = cv2.imread(os.path.join(path2,file))
    features = allfeatures(img)

    training.append(features)

training = np.array(training)
#training = preprocessing.scale(training)
#print training



y = [1 for i in range(totalpositive)] + [0 for i in range(totalnegative)]
#print y
#print total
clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(training,y)




print("testing positive samples--------")
for file in dirs[-5:]:

    img = cv2.imread(os.path.join(path,file))
    features = allfeatures(img)

    print(file + "  is  "+ str(clf.predict(features)))

print("testing negative samples----------")
for file in dirs2[-20:]:
    img = cv2.imread(os.path.join(path2,file))
    features = allfeatures(img)

    print(file + "  is  "+ str(clf.predict(features)))




