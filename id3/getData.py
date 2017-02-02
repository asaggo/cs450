class GetData(object):
    def __init__(self):
        self.data = []
        self.file = open("test.txt",'r')
    def parseFile(self):
        for line in self.file:
            temp = line.split()
            self.data.append(temp)

