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


    def getSet(self,data,index):
        elements = []
        if (not data):
            return None

        for row in data:
            elements.append(row[index])
        return (list(set(elements)),elements)


    def bestAttribute(self, data, fIndexes, tIndex, used):
        if (not data):
            return None
        targetType, targetList = self.getSet(data,tIndex)

        bestAttr = []
        for f in fIndexes:
            types, fColumn = self.getSet(data,f)
            entropies = []
            for t in types:
                weighted = 0
                entropy = 0
                count = np.zeros(len(targetType))

                for type,target in zip(fColumn,targetList):
                    if t == type:
                        count[targetType.index(target)] += 1

                for c in count:
                    entropy += self.calcEnt(c/sum(count))
                weighted += entropy * sum(count) / len(fColumn)
                entropies.append(weighted)
            bestAttr.append((sum(entropies),(f,types)))


        tuple = min(bestAttr)

        return tuple[1]



    def recur(self,data,node,used, fIndexes, tIndex):
        if (not data):
            return None
        node.level += 1
        colIndex, types = self.bestAttribute(data, fIndexes, tIndex, used)
        used[colIndex] = 1

        for t in types:
            newNode = node.grow(colIndex, node.level + 1, t)
            newData = self.cut(data,colIndex,t)

            if (node.level < 5):
                self.recur(newData,newNode,used,fIndexes,tIndex)


    def cut(self,data,colIndex,type):
        if (not data):
            return None
        newData = []
        for row in data:
            if (row[colIndex] == type):
                newData.append(row)
        return newData



class Node:
    def __init__(self,colIndex = -1, level = 0, types=''):
        self.children = []
        self.level = level
        self.types = types

    def grow(self,colIndex, level, types):
        temp = Node(colIndex,level,types)
        self.children.append(temp)
        return temp

    def predict(self):
        pass


dt = getData.GetData()
dt.parseFile()
id3 = ID3(dt.data)
data = id3.data
node = Node()
used = np.zeros(len(data[0])-1)
fIndexes = [0,1,2]
tIndex = 3
id3.recur(data,node,used, fIndexes, tIndex)