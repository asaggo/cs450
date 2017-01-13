class Classifier(object):
    def train(self,data_train,target_train):
        pass
    def predict(self,data_test):
        list = []
        for row in data_test:
            result = self.classify(row)
            list.append(result)
        return list
    def classify(self,row):
        return 0