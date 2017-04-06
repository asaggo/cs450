import getData
import random
from math import exp

accuracy = 0
dt = getData.GetData()
dt.parseFile()
#dt.data is 2 dimensional array.
dt.normalizeData()   #scaling


targets = []
for row in dt.data:
    targets.append(row[-1])




########bottom line is that we need to keep our weights, but renew inputs (activation, h), and weights every time when we go forward#############

class Neuron(object):  #numWeights = how many weights do we need for this particular neuron?
    def __init__(self,numWeights,positionInLayer): #changed: got rid of inputs in parameter

        self.weights = [round(random.uniform(-2.0,2.0),1) for x in range(numWeights)]
        self.activation = 0
        self.h = 0
        self.position = positionInLayer + 1 #need to consider bias node as the first position
        self.error = 0
        self.target = []


    def getActivation(self,inputs): #When it is first layer, inputs (array) should be coming from dt.data.
                                    #after that, inputs will be the activations from the previous layer.

        #make sure that they start from initial value
        self.activation = 0
        self.h = 0


        for i in range(len(inputs)):
            self.h += inputs[i]*self.weights[i]

        self.activation = 1/(1 + exp(-self.h))


    def calcErrorOutput(self,target): #calculate error when the node is on the output layer
        self.error = 0
        #print "error: ",self.error
        #print "target: ", target
        #print "activation: ", self.activation
        #print "activation  - target: ", self.activation-float(target)
        self.error = self.activation * (1-self.activation) * (self.activation - float(target))
        #print "error after calculation: ", self.error

    def calcErrorHidden(self,nextLayer): #calculate error when the node is on the hidden layer
        self.error = 0
        self.error = self.activation * (1-self.activation) * self.getSumWeightError(nextLayer)


    def getSumWeightError(self,nextLayer): #get sum of multiplication of weight and error
        sum = 0
        for neuron in nextLayer:
            sum += neuron.weights[self.position]*neuron.error
        return sum



#######input is not included in the layers. Hidden layer + output is inside of layers.

class Network(object): #numInputs should be len(dt.data[0]) or something like that
    def __init__(self, numInputs, numHiddenLayers, numNeuron): #numNeuron = in each layer how many nodes do you want? ex:I have three hidden layers -> [2,3,2]

        temp = [x+1 for x in numNeuron] ##temp is for adding one to each element in numNeuron so that we can create one more weight for bias node
        self.numLayers = numHiddenLayers + 1  # adds output layer as one of the layers
        #numWeights will be used in determining how many weights do we need for a specific neuron
        #numWeights = []
        self.numWeights = [numInputs] + temp #ex: [4,2,3,2] there are 4 inputs
        self.numNeurons = numNeuron + [len(dt.targetTypes)] #ex: [2,3,2,2] there are 2 output cases (0 or 1 or something like that)

        self.layers = [[Neuron(self.numWeights[i],nTimes) for nTimes in range(self.numNeurons[i])] for i in range(self.numLayers)] #ex: i = 0,1,2
                        #to access each neuron, we can call layers[i][j]

        self.learningRate = .1

    def calcLayer(self,inputs, whichLayer, target):  #recursive function. At first whichLayer = 0.
        newInputs = []
        temp = None #initialize
        temp = [-1] + inputs #includes bias node

        for neuron in self.layers[whichLayer]:
            neuron.target = target #now, all neurons will have target even though we will only use when it is output node.
            neuron.getActivation(temp)
            newInputs.append(neuron.activation)
        whichLayer += 1

        if whichLayer == len(self.layers):
            return
        else: #this should be whichLayer == len(self.layers)
            self.calcLayer(newInputs, whichLayer, target)



    def calcReverseLayer(self,whichLayer): #recursive function. At first whichLayer is the last layer's index

        for neuron in self.layers[whichLayer]:
            if whichLayer == self.layers.index(self.layers[-1]): #if it is outputlayer node
                neuron.calcErrorOutput(neuron.target[neuron.position-1]) #needs to subtract 1 because at the beginning, we added 1 for bias node
                                                                         #but actual index of target is one less

            else: #if it is one of hidden layer node
                neuron.calcErrorHidden(self.layers[whichLayer+1])

        whichLayer -= 1
        if whichLayer < 0:
            return
        else:
            self.calcReverseLayer(whichLayer)



    def changeWeights(self,neuron,inputs):
        #print len(inputs)
        #print len(neuron.weights)
        #print inputs
        for i in range(len(neuron.weights)):
            #print "i: ",i
            #print "weights[i]: ", neuron.weights[i]
            #print "input[i]: ",inputs[i]
            #print "activation: ", neuron.activation
            #print "learning Rate: ",self.learningRate
            neuron.weights[i] -= float(inputs[i]) * float(neuron.error) * float(self.learningRate)




    def updateWeights(self,inputs):
        activations = [[-1] + inputs]
        for layer in self.layers:
            temp = []
            temp.append(-1)
            for neuron in layer:
                temp.append(neuron.activation)
            #print temp
            activations.append(temp)

        #print activations
        for i in range(self.numLayers):
            for neuron in self.layers[i]:
                self.changeWeights(neuron,activations[i])




    def testNeuron(self):
        for neuron in self.layers[0]:
            print "error: ", neuron.error
            print "activation: ", neuron.activation



    def getOutput(self,layer):
        output = []
        for neuron in layer:
            output.append(neuron.activation)

        return output.index(max(output))






network = Network(len(dt.data[0]),1,[3])


##########test functions############
def printWeights():
    for layer in network.layers:
        for neuron in layer:
            print neuron.weights

def printActivations(input):
    print input #this doesn't include -1
    for layer in network.layers:
        temp = []
        for neuron in layer:
            temp.append(neuron.activation)
        print temp

def printError():
    for layer in network.layers:
        temp = []
        for neuron in layer:
            temp.append(neuron.error)
        print temp

def printInput(inputs):
    print inputs
####################################


####to get accuracy####
def isCorrect(outputLayer, target):
    intTarget = []
    output = []
    for neuron in outputLayer:
        output.append(neuron.activation)
    for value in target:
        intTarget.append(int(value))

    #print "output index: ",output.index(max(output))
    #print "target index: ", intTarget.index(max(intTarget))

    if output.index(max(output)) == intTarget.index(max(intTarget)):
        return 1
    else:
        return 0
#######################




acc = 0
#for nTimes in range(1000): #100 epochs
while acc < 98:
    correct = 0
    for row in dt.data:
        #print "start weights: ",printWeights()
        #print "inputs: ", printInput(row[:-1])

        network.calcLayer(row[:-1],0,row[-1]) #sends inputs, whichLayer index (which is 0 at first), target (ex:[0,1])
        #print "after go forward, activations: ", printActivations(row[:-1])


        network.calcReverseLayer(network.numLayers-1) #sends the last layer's index
        #print "after back propagation, errors: ", printError()


        network.updateWeights(row[:-1])
        #print "after updated: ", printWeights()

        correct += isCorrect(network.layers[-1],row[-1])

    acc = float(correct) / float(len(dt.data)) * 100.0
    print acc






def getAllOutput(weights):
    outputs = []
    for row in dt.data:
        neuron = Neuron(row,weights)
        neuron.getActivation()
        outputs.append(neuron.output)
    return outputs




'''

while(accuracy <= 94):

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
'''