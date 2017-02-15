from sklearn import preprocessing
import numpy as np

class GetData(object):
    def __init__(self):
        self.temp = []
        self.dataWOTarget = []
        self.targets = []
        self.targetTypes = []
        self.data = []
        self.file = open("pima.txt",'r')
    def parseFile(self):
        for line in self.file:
            self.temp.append(line.replace('\n','').split(',',len(line)))

        for row in self.temp:
            self.dataWOTarget.append(row[:-1])
            self.targets.append(row[-1])

        self.targetTypes = set(self.targets)



        #[['0','0'],['0','0'],...]
        zerosTargets = [['0'] * len(self.targetTypes) for i in range(len(self.targets))]



        #[['0','1'],['1','0'],....]
        for i,value in zip(range(len(self.targets)), self.targets):
            zerosTargets[int(i)][int(value)] = '1'

        self.targets = zerosTargets





    def normalizeData(self):
        self.dataWOTarget = preprocessing.normalize(self.temp,norm='l2')
        for row, target in zip(self.dataWOTarget,self.targets):
            self.data.append(list(row)+[target])

