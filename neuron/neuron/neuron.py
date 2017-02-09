import getData
import random

accuracy = 0
dt = getData.GetData()
dt.parseFile()
#dt.data is 2 dimensional array.
dt.normalizeData()   #scaling
threshold = 0

#for row in dt.data:
#    print len(row)


weights = [round(random.uniform(-2.0,2.0),1) for x in range(len(dt.data[0]))]
targets = []
for row in dt.data:
    targets.append(row[-1])



class Neuron(object):
    def __init__(self,row, weights):
        #self.weights = None
        self.weights = weights
        self.temp = [-1]+row[:-1]
        self.input = []
        for i in range(len(self.temp)):
            self.input.append(float(self.temp[i])) #changing all string elements to float
        self.activation = 0
        self.output = -1
        self.target = row[-1]

    def getActivation(self):
        for i in range(len(self.input)):
            self.activation += float(self.input[i])*float(self.weights[i])
        if self.activation >= threshold:
            self.output = 1
        else:
            self.output = 0



    def modifyWeights(self):
        learningRate = 5
        newWeights = []
        for i in range(len(self.weights)):
            #print len(self.input)
            newWeights.append(float(self.weights[i]) - learningRate * (float(self.output) - float(self.target))*float(self.input[i]))

        for i in range(len(self.weights)):
            self.weights[i] = newWeights[i]
        #print self.weights


def getAllOutput(weights):
    outputs = []
    for row in dt.data:
        neuron = Neuron(row,weights)
        neuron.getActivation()
        outputs.append(neuron.output)
    return outputs


def checkAccuracy(outputs,targets):
    correct = 0
    for i in range(len(outputs)):
        if int(outputs[i]) == int(targets[i]):
            correct += 1

    return float(correct)/len(targets)





while(accuracy <= 50):

    for row in dt.data:
        isModified = False


        neuron = Neuron(row,weights)
        neuron.getActivation()
        if (int(neuron.output) != int(neuron.target)):
            neuron.modifyWeights()
            isModified = True

        #weights = None
        weights = neuron.weights
        #print weights
        #print neuron.output, " ", neuron.target, " ", isModified


    outputs = []
    outputs = getAllOutput(weights)

    accuracy = checkAccuracy(outputs,targets)*100
    #print accuracy, "%"

print accuracy, "%"
