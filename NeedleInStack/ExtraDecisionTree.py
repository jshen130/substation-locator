__author__ = 'zhengyiwang'
import cv2
import numpy as np
import os
import featureExtraction
from sklearn.externals import joblib
from sklearn.tree import DecisionTreeClassifier
import shutil


def allfeatures(img):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return np.hstack((featureExtraction.colorCube(img_HSV), featureExtraction.getLineHist(img_HSV)))

def train_edt(files_pos, files_neg):
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

    print "\nTraining Decision Tree..."
    label = np.hstack((np.ones(cnt_total_pos), np.zeros(cnt_total_neg)))
    trained_edt = DecisionTreeClassifier()
    trained_edt.fit(training, label)
    joblib.dump(trained_edt, trained_edt_filename)
    print "Decision Tree trained!! Model saved as: " + trained_edt_filename

    return trained_edt


def test_edt_training(trained_EDT, files_pos, files_neg):
    print("\nTesting positive samples--------")
    for file in files_pos:
        img = cv2.imread(file)
        print file + "  is  " + str(trained_EDT.predict(allfeatures(img).reshape((1, -1))))

    print("\nTesting negative samples--------")
    for file in files_neg:
        img = cv2.imread(file)
        print file + "  is  " + str(trained_EDT.predict(allfeatures(img).reshape((1, -1))))


def test_sunnyvale(trained_EDT, folder):
    print "\nFinding substation for the SunnyVale...."
    for file in folder:
        img = cv2.imread(file)
        result = trained_EDT.predict(allfeatures(img).reshape((1, -1)))[0]
        destination = os.path.expanduser("~/Workshop/find_substation_Extradt"+file[26:])
        if result == 1:
            shutil.copyfile(file, destination)
            print file + "  is  positive"


if __name__ == "__main__":
    trained_edt_filename = "trained_edt.pkl"
    path_pos = "../training-pos"
    path_neg = "../training-neg"
    path_sunnyvale = "../../sunnyvale_region_map"
    files_pos = [os.path.join(path_pos, f) for f in os.listdir(path_pos)]
    files_neg = [os.path.join(path_neg, f) for f in os.listdir(path_neg)]
    file_sunnyvale = [os.path.join(path_sunnyvale, f) for f in os.listdir(path_sunnyvale)]
    n_test_pos = 1
    n_test_neg = 1

    if os.path.exists(trained_edt_filename):
        print "Found a trained Decision Tree saved as '" + trained_edt_filename + "'. Loading model!"
        trained_EDT = joblib.load(trained_edt_filename)
    trained_EDT = train_edt(files_pos[1:-n_test_pos], files_neg[1:-n_test_neg])
    #test_DT_training(trained_DT, files_pos[-n_test_pos:], files_neg[-n_test_neg:])
    test_sunnyvale(trained_EDT, file_sunnyvale)

