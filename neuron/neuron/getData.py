from sklearn import preprocessing


class GetData(object):
    def __init__(self):
        self.temp = []
        self.dataWOTarget = []
        self.targets = []
        self.data = []
        self.file = open("pima.txt",'r')
    def parseFile(self):
        for line in self.file:
            self.temp.append(line.replace('\n','').split(',',len(line)))

        for row in self.temp:
            self.dataWOTarget.append(row[:-1])
            self.targets.append(row[-1])

    def normalizeData(self):
        self.dataWOTarget = preprocessing.normalize(self.temp,norm='l2')
        for row, target in zip(self.dataWOTarget,self.targets):
            self.data.append(list(row)+[target])
