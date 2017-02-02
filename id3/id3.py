import getData
import numpy as np

class ID3(object):
    def __init__(self,data):
        self.data = data

    def calcEnt(self,p):
        if p != 0:
            return -p*np.log2(p)
        else:
            return 0


    def getSet(self,index):
        elements =[]
        for row in self.data:
            elements.append(row[index])
        return (list(set(elements)),elements)


    def getEntropy(self, fIndex, tIndex):
        targetType, targetList = self.getSet(tIndex)
        attrType, attrList = self.getSet(fIndex)

        entropies = []
        for eachType in attrType: #for example, good, average, low
            entropy = 0
            weightedAve = 0
            count = np.zeros(len(targetType))
            for index in range(len(attrList)): #go through whole list of attrList
                if attrList[index] == eachType:
                    count[targetType.index(targetList[index])] += 1
            for c in count:                      #if the target type is yes and no, count array will have [5,3] or something like that
                entropy += self.calcEnt(c/sum(count)) #this is just a number counted. How many yes and no are there.
            weightedAve = entropy * sum(count) / len(attrList) #pre-weighted
            entropies.append(weightedAve)

        return sum(entropies)




dt = getData.GetData()
dt.parseFile()
id3 = ID3(dt.data)
csEnt = id3.getEntropy(0,3)
incomeEnt = id3.getEntropy(1,3)
collEnt = id3.getEntropy(2,3)

print csEnt
print incomeEnt
print collEnt