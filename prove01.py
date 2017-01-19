from sklearn import datasets
from sklearn.cross_validation import train_test_split as tts
import classifier
import random

from copy import copy, deepcopy


iris = datasets.load_iris()
data_train, data_test, target_train, target_test = tts(iris.data, iris.target, train_size=.7, random_state=random.randint(100,500))
#
# def compare(list, target_test):
#     count = 0
#
#     for i in range(len(target_test)):
#         if (list[i] == target_test[i]):
#             count += 1
#     return count

cf = classifier.Classifier()
cf.train(data_train,target_train,target_test)
k = raw_input("How many neighbors? ")
result = []
result = cf.predict(data_test,int(k)) #has 0,0,1 or 0,1,2 or something like that
cf.compare()



#count = compare(list,target_test)
#percent = count/float(len(target_test))
#percent = round(percent*100,2)
#print "accuracy:",percent,"%"

