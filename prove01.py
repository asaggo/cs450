from sklearn import datasets
from sklearn.cross_validation import train_test_split as tts
import classifier
import random
iris = datasets.load_iris()
data_train, data_test, target_train, target_test = tts(iris.data, iris.target, train_size=.7, random_state=random.randint(100,500))

def compare(list, target_test):
    count = 0

    for i in range(len(target_test)):
        if (list[i] == target_test[i]):
            count += 1
    return count

cf = classifier.Classifier()
cf.train(data_train,target_train)
list = cf.predict(data_test)
count = compare(list,target_test)
percent = count/float(len(target_test))
percent = round(percent*100,2)
print "accuracy:",percent,"%"

