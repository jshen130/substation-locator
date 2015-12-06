__author__ = 'zhengyiwang'
from sklearn import svm
import numpy as np
import cv2
import features1
from sklearn import preprocessing
from sklearn import datasets
from sklearn import metrics

from sklearn.tree import DecisionTreeClassifier
from naiveBayesClassifier.classifier import Classifier
from sklearn.ensemble import ExtraTreesClassifier



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
TestCase = 10

print("----------positive")
totalpositive = 0
for file in dirs[1:-TestCase]:
    totalpositive += 1
    img = cv2.imread(os.path.join(path,file))
    features = allfeatures(img)

    training.append(features)
    print features

print"-----------negetive"
totalnegative = 0
for file in dirs2[1:-TestCase]:
    totalnegative += 1
    img = cv2.imread(os.path.join(path2,file))
    features = allfeatures(img)

    training.append(features)
    print features

training = np.array(training)
#training = preprocessing.scale(training)

y = [1 for i in range(totalpositive)] + [0 for i in range(totalnegative)]
#print y
#print total

# SVM
#svm_classifier = svm.SVC(kernel='linear', C = 1.0)
#svm_classifier.fit(training,y)

#decision tree
decisionTree_classifier = DecisionTreeClassifier()
decisionTree_classifier.fit(training, y)

#naive bayesian
#not working
#naiveBayesian_classifier = Classifier(training, y)

#ExtraDecisionTree
etree_classifier = ExtraTreesClassifier()
etree_classifier.fit(training, y)

#feature importance :
print("feature importance or Extra desicion tree")

print(etree_classifier.feature_importances_)


print("feature importance or Decision tree")
print(decisionTree_classifier.feature_importances_)
#print(svm_classifier.feature_importances_)

print("testing positive samples--------")
for file in dirs[-TestCase:]:

    img = cv2.imread(os.path.join(path,file))
    features = allfeatures(img)
    #result = svm_classifier.predict(features)
    result = decisionTree_classifier.predict(features)
    #result = naiveBayesian_classifier.classify(features)
    #result = etree_classifier.predict(features)


    print(file + "  is  "+ str(result))

print("testing negative samples----------")
for file in dirs2[-TestCase:]:
    img = cv2.imread(os.path.join(path2,file))
    features = allfeatures(img)
    #result = svm_classifier.predict(features)
    result = decisionTree_classifier.predict(features)
    #result = naiveBayesian_classifier.classify(features)
    #result = etree_classifier.predict(features)
    print(file + "  is  "+ str(result))




