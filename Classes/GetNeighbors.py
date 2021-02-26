import operator
from Classes.EucDis import EucDis

class GetNeighbors:
    def getNeighors(self, trainingSet,testInstance,k):
        distances = []
        length = len(testInstance)-1
        for x in range(len(trainingSet)):
            dist = EucDis.euclideanDistance(testInstance, trainingSet[x],length)
            distances.append((trainingSet[x],dist))
        distances.sort(key=operator.itemgetter(1))
        neighbors = []
        for x in range(k):
            neighbors.append(distances[x][0])
        return neighbors