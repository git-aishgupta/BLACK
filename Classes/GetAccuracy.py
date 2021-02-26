from operator import itemgetter 
class GetAccuracy:
    def getAccuracy(self, predictions,partClass):
        b = itemgetter(0)(predictions)
        for x in range(len(b)):
            c = itemgetter(x)(b)
            d = itemgetter(0)(c)

            if d == partClass :
                predicted_value = c   
                predicted_value_final = itemgetter(1)(predicted_value)
                accuracy = (predicted_value_final/5)*100
        return accuracy