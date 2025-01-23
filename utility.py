import numpy as np
from scipy.stats import entropy

from state import State

#################//Functions//##################################################
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def expectedValue(values, weights):
    #print("Expected value")
    #print("Values", values.shape)
    #print("Weights", weights.shape)
    #print(weights[:][0][:].shape)
    #print("######################")
    weightedValues = values@weights
    for rowIdx in range(len(weightedValues)):
        weightedValues[rowIdx] = weightedValues[rowIdx].sum()

    return weightedValues

def entropy2D(nparray):
    #print("Entropy")
    #print(nparray.shape, "should be two dimensional.")
    #print("*******************")
    entropy = []
    for row in nparray:
        entropy.append(-np.sum(row * np.log(softmax(row)))) # by default it retunrs the Shannon entropy on base e but it can be changes with the "base" parameter
    return np.array(entropy)

def entropy3D(nparray):
    entropy = []
    for row in nparray:
        entropy.append(entropy2D(row))
    return np.array(entropy)

#def divergance(nparray1, nparray2):
#    return entropy(nparray1, nparray2) #Kullback-Leibler divergence on base e by default

#def getPosteriors(states_probs, observations_probs, a_matrix):
    #the aMatrix has the probabilities for the observations conditioned to the inner states
#   return (states_probs*a_matrix)/observations_probs

def conditionalProbability(x, y, yConditionedToX):
    #all parameters have to be probability distributions for the corresponding variables
    return (x * yConditionedToX)/y

###################################################################################################
###################################################################################################
###################################################################################################

######################//Sets//#####################################################################
class Set():
    def __init__(self):
        self.set = []

    def add(self, element):
        self.set.append(element)

    def remove(self, element):
        self.set.remove(element)

    def checkElement(self, element):
        for elem in self.set:
            if elem.equals(element):
                return True
        return False

class OrderedSet():

    def __init__(self):
        self.values = []
        self.keys = []

    def add(self, key: State, value: int):
        if not self.checkElement(key):
            idx = 0
            while idx < len(self.values) and self.values[idx] <= value:
                idx = idx + 1
            new_keys = self.keys[0:idx]
            new_keys.append(key)
            for elem in self.keys[idx+1:]:
                new_keys.append(elem) 
            self.keys = new_keys

            new_vals = self.values[0:idx]
            new_vals.append(value)
            for elem in self.values[idx+1:]:
                new_vals.append(elem)  
            self.values = new_vals
        else:
            idx = self.getIndex(key)
            if (self.values[idx] > value):
                self.values.pop(idx)
                self.keys.pop(idx)
                self.add(key, value)

    def retrieve(self, order="lower"):
        if order == "higher":
            val = self.keys[-1]
            self.values.pop(-1)
            self.keys.pop(-1)
        elif order == "lower":
            val = self.keys[0]
            self.values.pop(0)
            self.keys.pop(0)
        else:
            raise Exception("Wrong order from getting element out of the queue.")
        return val
    
    def checkElement(self, element):
        for elem in self.keys:
            if elem.equals(element.getState()):
                return True
        else:
            return False
        
    def getIndex(self, element):
        idx = 0
        for elem in self.keys:
            if elem.equals(element.getState()):
                return idx
            else:
                idx = idx + 1
        raise Exception("Element not in ordered set.")
    
    def isEmpty(self):
        return len(self.keys) == 0

###################################################################################################
###################################################################################################
###################################################################################################