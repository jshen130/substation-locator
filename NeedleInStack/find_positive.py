__author__ = 'zhengyiwang'
import os, sys
import shutil



# This would print all the files and directories

def rename(dirs):
    for file in dirs:
        os.rename(os.path.join(path,file), os.path.join(path,file+".png"))

    path_neg = "../training-neg"
    path_sunnyvale = "../../sunnyvale_region_map"

def copyToNewFolder(filepath, positive):
    if positive:
        shutil.copyfile(filepath, "../../find_substation/")

def movefile(filepath, destination):
    shutil.move(filepath, destination)

def find_intersection(path1, path2):
    dirs1 = os.listdir(path1)
    dirs2 = os.listdir(path2)
    intersec = list(set(dirs1) & set(dirs2))
    print "intersection is "
    print len(intersec)
    for file in intersec:
        destination = os.path.expanduser("~/Workshop/sunnyvale_positive/"+file)
        print destination
        shutil.copyfile("../../find_substation_svm/"+file, destination)

    return intersec

def intersectionOfList(a,b):
    intersec = set(a) & set(b)
    print len(intersec)
    for file in intersec:
        destination = os.path.expanduser("~/Workshop/berkeley_positive_edt/"+file[20:])
        print destination
        shutil.copyfile("../../"+file, destination)

def fileInB(a,b):
    for f in b:
        if f in a:
            #print f
            destination = os.path.expanduser("~/Workshop/berkeley_positive/"+f[20:])
            print destination
            shutil.copyfile("../../"+f, destination)

def countmissing(path_result):
    dirs = os.listdir( path_result )

    true_positive = open("true_positive")
    missing = 0

    for file in true_positive:
        file = file.strip()
        if file not in dirs:
            missing += 1
            print file
    print "\ntrue positive missing:"
    print missing

def addpositive(src):
    positive = open("true_positive")
    destination = "../training-pos"
    for i in positive:
        i = i.strip()
        shutil.copyfile(os.path.join(src, i), os.path.join(destination , i))

def addnegative(src):
    newnegative = open("newnegative")
    needtoadd = []
    path_neg = "../training-neg"
    for line in newnegative:
        needtoadd.append(line.strip())
    for i in needtoadd:
        print i
        shutil.copyfile(os.path.join(src, i), os.path.join(path_neg , i))

def vote(l1, l2, l3):
    allfile = set(l1) | set(l2) | set(l3)
    c = 0
    for file in allfile:
        vote = 0
        if file in l1:
            vote += 1
        if file in l2:
            vote += 1
        if file in l3:
            vote += 1
        if vote >= 2:
            destination = os.path.expanduser("~/Workshop/berkeley_positive/"+file[20:])
            c += 1
            print destination
            #shutil.copyfile("../../"+file, destination)
    print c

def vote_algorithm():
    bdt = open("b_dt.txt")

    list_bdt = []
    for line in bdt:
        list_bdt.append(line.strip()[6:])
    print "positive in berkeley, DT"
    print len(list_bdt)

    bdt = open("b_svm.txt")

    list_bsvm = []
    for line in bdt:
        list_bsvm.append(line.strip()[6:])
    print "positive in berkeley , SVM"
    print len(list_bsvm)

    bEdt = open("b_edt.txt")
    list_bedt = []
    for line in bEdt:
        list_bedt.append(line.strip()[6:])
    print "positive in berkeley, EDT"
    print len(list_bedt)

    vote(list_bedt,list_bdt,list_bsvm)

if __name__ == "__main__":
    path_sunnyvale = "../../sunnyvale_region_map"

    path_dt = "../../find_substation_dt_trainningmore"
    path_svm = "../../find_substation_svm"
    path_Edt = "../../find_substation_Extradt"


    # Open a file
    #path = os.path.expanduser("~/Workshop/substation-locator/trainingdata")


    #print needtoadd



    #intersect = find_intersection(path_dt, path_svm)
    #countmissing(os.listdir(path_dt))
    '''
    f= open("b_svm.txt")
    c = 0
    for line in f:
        list1 = line.strip().split("../../")
        print len(list1)

    print list1[1]
    print  list2[1]

    #intersectionOfList(list,list2)
    intersec = list(set(list1) & set(list2))
    fileInB(intersec,list2)
    '''


    vote_algorithm()



    #addpositive(path_dt)
    #addnegative(path_dt)
    #countmissing(path_svm)
#    for file in os.listdir(path_neg):
   #     if file.startswith("sunny"):
   #         print file
            #movefile( os.path.join(path_neg, file),os.path.join(path_sunnyvale,file))


84351
278307
15258
17608
80
0
1840
0
0
3731
0
0
0
0
0
211
0
0
7756
458
0
0
0
0
0
0
0
