import csv
import random
class GetData:
    def getData(filename,split,trainingSet = [], testSet = []):
        with open(filename, 'r') as csvfile:
            lines = csv.reader(csvfile)
            dataset = list(lines)
            for x in range(len(dataset)-1):
                for y in range(2):
                    dataset[x][y] = dataset[x][y]
                if random.random() < split:
                    return trainingSet.append(dataset[x])
                else:
                    return testSet.append(dataset[x])