import getData
import random
from math import exp

accuracy = 0
dt = getData.GetData()
dt.parseFile()
#dt.data is 2 dimensional array.
dt.normalizeData()   #scaling
threshold = 0

#for row in dt.data:
#    print len(row)


#weights = [round(random.uniform(-2.0,2.0),1) for x in range(len(dt.data[0]))]
targets = []
for row in dt.data:
    targets.append(row[-1])




########bottom line is that we need to keep our weights, but renew inputs (activation, h), and weights every time when we go forward#############

class Neuron(object):  #numWeights = how many weights do we need for this particular neuron?
    def __init__(self,numWeights): #changed: got rid of inputs in parameter

        self.weights = [round(random.uniform(-2.0,2.0),1) for x in range(numWeights)]
        #self.inputs = []
        self.activation = 0
        self.h = 0


        #self.temp = [-1] + inputs[:-1]
        #self.input = []
        #for i in range(len(self.temp)):
        #    self.input.append(float(self.temp[i]))  # changing all string elements to float


        #self.output = -1
        #self.target = row[-1]


    def getActivation(self,inputs): #When it is first layer, inputs (array) should be coming from dt.data.
                                    #after that, inputs will be the activations from the previous layer.

        #make sure that they start from initial value
        self.activation = 0
        self.h = 0


        for i in range(len(inputs)):
            #print "w: ", self.weights
            #print "I: ", inputs
            self.h += inputs[i]*self.weights[i]

        self.activation = 1/(1 + exp(-self.h))

        #if self.activation >= threshold:
        #    self.output = 1 #later, maybe it needs a change (1/(1+e^h)x)) or something like that
        #else:
        #    self.output = 0



    def modifyWeights(self):
        learningRate = .1
        newWeights = []
        for i in range(len(self.weights)):
            #print len(self.input)
            newWeights.append(float(self.weights[i]) - learningRate * (float(self.output) - float(self.target))*float(self.input[i]))

        #for i in range(len(self.weights)):
        #    self.weights[i] = newWeights[i]
        self.weights = newWeights
        #print self.weights


#######input is not included in the layers. Hidden layer + output is inside of layers.

class Network(object): #numInputs should be len(dt.data[0]) or something like that
    def __init__(self, numInputs, numHiddenLayers, numNeuron = []): #numNeuron = in each layer how many nodes do you want? ex:I have three hidden layers -> [2,3,2]

        temp = [x+1 for x in numNeuron] ##temp is for adding one to each element in numNeuron so that we can create one more weight for bias node
        self.numLayers = numHiddenLayers + 1  # adds output layer as one of the layers
        #numWeights will be used in determining how many weights do we need for a specific neuron
        #numWeights = []
        self.numWeights = [numInputs] + temp #ex: [4,2,3,2] there are 4 inputs
        self.numNeurons = numNeuron + [len(dt.targetTypes)] #ex: [2,3,2,2] there are 2 output cases (0 or 1 or something like that)

        self.layers = [[Neuron(self.numWeights[i]) for nTimes in range(self.numNeurons[i])] for i in range(self.numLayers)] #ex: i = 0,1,2
                        #to access each neuron, we can call layers[i][j]


    def calcLayer(self,inputs, whichLayer):  #recursive function
        newInputs = []
        temp = None #initialize
        temp = [-1] + inputs #includes bias node

        for neuron in self.layers[whichLayer]:
            neuron.getActivation(temp)
            newInputs.append(neuron.activation)
        whichLayer += 1

        if whichLayer == len(self.layers):
            return
        else: #this should be whichLayer == len(self.layers)
            self.calcLayer(newInputs, whichLayer)

    def getHighest(self,outputLayer):
        output = []
        for neuron in outputLayer:
            output.append(neuron.activation)

        print output
        return output.index(max(output)) #return which index has highest activation(output)


network = Network(len(dt.data[0]),2,[2,3])
for row in dt.data:
    network.calcLayer(row[:-1],0)
    highestIndex = network.getHighest(network.layers[-1])
    print highestIndex













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