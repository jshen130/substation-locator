__author__ = 'zhengyiwang'
import cv2
import numpy as np
import os
import featureExtraction
from sklearn import svm
from sklearn.externals import joblib
import shutil
import os

def allfeatures(img):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return np.hstack((featureExtraction.colorCube(img_HSV), featureExtraction.getLineHist(img_HSV)))

def train_SVM(files_pos, files_neg):
    training = np.empty((len(files_pos) + len(files_neg), len(allfeatures(cv2.imread(files_pos[0])))), dtype=int)

    print "Obtaining features from " + str(len(files_pos)) + " positive training samples... "
    cnt_total_pos = 0
    for file in files_pos:
        training[cnt_total_pos] = allfeatures(cv2.imread(file))
        cnt_total_pos += 1
        print str(cnt_total_pos) + ", ",

    print "\nObtaining features from " + str(len(files_neg)) + " negative training samples... "
    cnt_total_neg = 0
    for file in files_neg:
        training[cnt_total_pos + cnt_total_neg] = allfeatures(cv2.imread(file))
        cnt_total_neg += 1
        print str(cnt_total_neg) + ", ",

    print "\nTraining SVM..."
    label = np.hstack((np.ones(cnt_total_pos), np.zeros(cnt_total_neg)))
    trained_svm = svm.SVC(kernel='linear', C=1.0)
    trained_svm.fit(training, label)
    joblib.dump(trained_svm, trained_svm_filename)
    print "SVM trained!! Model saved as: " + trained_svm_filename

    return trained_svm


def test_SVM_training(trained_svm, files_pos, files_neg):
    print("\nTesting positive samples--------")
    for file in files_pos:
        img = cv2.imread(file)
        print file + "  is  " + str(trained_svm.predict(allfeatures(img).reshape((1, -1))))

    print("\nTesting negative samples--------")
    for file in files_neg:
        img = cv2.imread(file)
        print file + "  is  " + str(trained_svm.predict(allfeatures(img).reshape((1, -1))))


def test_sunnyvale(trained_svm, folder):
    print "\nFinding substation for the SunnyVale...."
    for file in folder:
        img = cv2.imread(file)
        result = trained_svm.predict(allfeatures(img).reshape((1, -1)))[0]
        destination = os.path.expanduser("~/Workshop/find_substation_svm/"+file[26:])
        if result == 1:
            shutil.copyfile(file, destination)
            print file + "  is  positive"


def test_berkely(trained_svm, folder):
    berkely_positive_svm = open("b_svm.txt", "w")
    print "\nFinding substation for the SunnyVale...."
    for file in folder:
        img = cv2.imread(file)
        result = trained_svm.predict(allfeatures(img).reshape((1, -1)))[0]
        destination = os.path.expanduser("~/Workshop/find_substation_svm/"+file[26:])
        if result == 1:
            #shutil.copyfile(file, destination)

            print file + "  is  positive"
            berkely_positive_svm.write(file + "\n")
    berkely_positive_svm.close()

if __name__ == "__main__":
    trained_svm_filename = "trained_svm.pkl"
    path_pos = "../training-pos"
    path_neg = "../training-neg"
    path_sunnyvale = "../../sunnyvale_region_map"
    path_berkeley= "../../berkeley_region_map"
    files_pos = [os.path.join(path_pos, f) for f in os.listdir(path_pos)]
    files_neg = [os.path.join(path_neg, f) for f in os.listdir(path_neg)]
    file_sunnyvale = [os.path.join(path_sunnyvale, f) for f in os.listdir(path_sunnyvale)]
    file_berkely = [os.path.join(path_berkeley, f) for f in os.listdir(path_berkeley)]


    n_test_pos = 1
    n_test_neg = 1

    if os.path.exists(trained_svm_filename):
        print "Found a trained SVM saved as '" + trained_svm_filename + "'. Loading model!"
        trained_svm = joblib.load(trained_svm_filename)
    trained_svm = train_SVM(files_pos[1:-n_test_pos], files_neg[1:-n_test_neg])
    #test_SVM_training(trained_svm, files_pos[-n_test_pos:], files_neg[-n_test_neg:])
    #test_sunnyvale(trained_svm, file_sunnyvale)
    test_berkely(trained_svm, file_berkely)

