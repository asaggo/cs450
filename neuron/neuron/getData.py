from sklearn import preprocessing


class GetData(object):
    def __init__(self):
        self.temp = []
        self.data = []
        self.file = open("pima.txt",'r')
    def parseFile(self):
        for line in self.file:
            self.temp.append(line.replace('\n','').split(',',len(line)))
    def normalizeData(self):
        self.data = preprocessing.normalize(self.temp,norm='l2')
        #print self.data
