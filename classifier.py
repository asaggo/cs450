
class Classifier(object):
    def __init__(self):
        self.distances = []
        self.percent = 0.0
        self.results = []

    def train(self,data_train,target_train,target_test):
        self.data_train = data_train
        self.target_train = target_train
        self.target_test = target_test

    def mostCommon(self,threeIndex):
        targetList = []
        for i in threeIndex:
            targetList.append(self.target_train[i])

        check = [0, 0, 0]
        for i in targetList:
            check[i] += 1

        mostCommonTarget = check.index(max(check))
        return mostCommonTarget



    def predict(self,data_test,k):
        # list = []
        # for row in data_test:
        #     result = self.classify(row)
        #     list.append(result)
        # return list

        for item in data_test: #send each row in data_test
            self.distances.append(self.getDistance(item, k)) # k == 3, the number of neighbor

        #print (self.distances)


        for each in self.distances:
            threeIndex = []
            for i in each:
                threeIndex.append(i[1])
            self.results.append(self.mostCommon(threeIndex))

        #After this, need tocompare results and target_test

    def compare(self):
        count = 0
        for i in range(len(self.results)):
            if (self.results[i] == self.target_test[i]):
                count += 1

        self.percent = round(100*(count / float(len(self.results))),2)
        print "Accuracy: " + str(self.percent) + "%"

    def getDistance(self,item,k):
        distance = []
        for row in range(len(self.data_train)): #all integer
            rowDistance = 0
            for col in range(len(self.data_train[row])):
                rowDistance += ((item[col]-self.data_train[row][col])**2)
            distance.append((rowDistance,row))
        distance.sort()
        return distance[:k]
        #self.distances.sort()

        #return self.distances






    def classify(self,row):
        return 0




