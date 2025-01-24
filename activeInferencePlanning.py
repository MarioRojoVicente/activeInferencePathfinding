from state import State
import numpy as np
from actions import DIRECTIONS, Move
from utility import softmax, entropy2D, entropy3D, expectedValue, conditionalProbability
import time

####################

#For "expectation" (Capital E in the G formula) refer to box 2.2
#The H in the G formula refers to the Shannon entropy
#Q refers to the aproximate postirior, meaning the expected observation on a time grater than the current

####################
class ActiveInferenceV2:

    h = None #heuristic
    goal = None #goal state
    statesList = [] #List of all posible ovservations
    aMatrix = [] #maps inner states with observations
    bMatrix = [] #transition matrix
    cVectors = [] #preferences for the observations
    dVectors = [] #prior probabilities of the initial state
    policiesPrios = []
    gVectors = [] #serves as the heuristic
    #eVectors = [] #stores epistemic value of states
    #cVectors = [] #stores the pragmatic value of states

    def __init__(self, initState, goalState, heuristic):
        self.h = heuristic
        self.goal = goalState
        self.init = initState
        self.generateAllPossibleStates(initState)
        #print(self.statesList)
        #print(len(self.statesList))
        #print("######################################")
        self.generateAMatrix()
        #print(self.aMatrix)
        #print("######################################")
        self.generateBMatrix()
        #print(self.bMatrix)
        #print("######################################")
        self.generateCVectors()
        #print(self.cVectors)
        #print("######################################")
        self.generateDVectors()
        #print(self.dVectors)
        #print("######################################")
        #self.generatePoliciesPrios()
        #print(self.gVectors)
        #print(self.gVectors.shape)
        #print("######################################")
        self.generateGVectors(self.dVectors)

    def generateAMatrix(self):
        self.aMatrix = np.identity(len(self.statesList))
        #for rowIdx in range(len(self.aMatrix)):
        #    self.aMatrix[rowIdx] = softmax(self.aMatrix[rowIdx])
        

    def generateBMatrix(self):
        #Each matrix shows the probabilities  under a different action choice
        for dir in DIRECTIONS.keys():
            self.bMatrix.append(np.zeros((len(self.statesList), len(self.statesList))))
            for stateIdx in range(len(self.statesList)):
                newState = Move(dir, 2, self.statesList[stateIdx]).result
                if newState != -1:#if move is valid
                    idx = 0
                    while not self.statesList[idx].equals(newState.getState()):
                        idx = idx + 1
                    self.bMatrix[-1][stateIdx][idx] = 1
                else:
                    self.bMatrix[-1][stateIdx][stateIdx] = 1

            #self.bMatrix[-1] = softmax(self.bMatrix[-1])

    def generateAllPossibleStates(self, initState: State):
        statesList = [initState]
        map = initState.getState()
        playerPos = initState.getPlayerPos(2)
        for row in range(len(map)):
            for col in range(len(map[0])):
                if map[row][col] == 0:
                    newMap =  initState.getState()
                    newMap[playerPos[0]][playerPos[1]] = 0
                    newMap[row][col] = 2
                    statesList.append(State(newMap))
        self.statesList = statesList
                    

    def generateCVectorsOld(self, goalState): #DEPRECATED
        self.cVectors = np.zeros(len(self.statesList))
        self.cVectors[0] = -1 #negative preference for initial state
        #positive preference for goal state
        idx = 0
        while not self.statesList[idx].equals(goalState.getState()):
            idx = idx + 1
        self.cVectors[idx] = 6
        ####################################
        self.cVectors = softmax(self.cVectors)
        self.cVectors = np.transpose(self.cVectors)

    def generateCVectors(self):
        self.cVectors = np.zeros(len(self.statesList))
        for elemidx in range(len(self.statesList)):
            self.cVectors[elemidx] = -self.evaluate(self.statesList[elemidx])
        
        ####################################
        #self.cVectors = softmax(self.cVectors)
        self.cVectors = np.transpose(self.cVectors)
    
    def updateCVectors(self, visitedStateIdx):
        self.cVectors[visitedStateIdx] = -len(self.statesList)

    def generateDVectors(self):
        #the D- vectors specify the prior probabilities for the initial states. The order of elements in  these vectors matches  those of the B-matrices.
        self.dVectors = np.zeros(len(self.statesList))
        self.dVectors[0] = 1 #marking initial state
        self.dVectors = np.transpose(self.dVectors)

    def generatePoliciesPrios(self):
        policiesPrios = np.array([[0,0,0,0,0]])
        for stateIdx in range(len(self.statesList)):
            row = []
            for dir in DIRECTIONS.keys():
                resultState = Move(dir, 2, self.statesList[stateIdx]).result
                row.append(self.evaluate(resultState))
            row = np.array(row)
            row = softmax(row)
            policiesPrios = np.append(policiesPrios, [row], axis=0)

        self.policiesPrios = policiesPrios[1:]
        #print(self.dVectors*np.transpose(self.policiesPrios))

    def generateGVectors(self, currentStates):
    
        #print("values", entropy2D(currentStates@self.bMatrix))
        #print("weights", np.transpose(currentStates@self.bMatrix))
        #print("t1", expectedValue(values=entropy2D(np.transpose(currentStates@np.array(self.bMatrix))), weights=np.transpose(currentStates@self.bMatrix)))
        #print("t2", entropy2D(currentStates@np.array(self.aMatrix)@np.array(self.bMatrix)))
        negativeEpistemicValue = expectedValue(values=entropy2D(np.transpose(currentStates@np.array(self.bMatrix))), weights=np.transpose(currentStates@self.bMatrix)) - entropy2D(currentStates@np.array(self.aMatrix)@np.array(self.bMatrix))
        pragmaticValues = np.log(self.aMatrix@softmax(self.cVectors)) #because they are independent from each other
        pragmaticWeights = currentStates@np.array(self.aMatrix)@np.array(self.bMatrix)
        pragmaticValue = expectedValue(values=pragmaticValues , weights=np.transpose(pragmaticWeights))
        self.gVectors = negativeEpistemicValue - pragmaticValue
        #print("Negative Epistemic Value", negativeEpistemicValue)
        #print("Pragmatic Value", pragmaticValue)
        #print("gVectors", self.gVectors)
        #print("cVectors", self.cVectors)


    def evaluate(self, child):
        #this function calculates the prios for the states
        if child == -1:
            return 10000
        return self.h.evaluate(child, self.goal)
        #return child.getPathLen() + self.h.evaluate(child.getPlayerPos(2), self.goal.getPlayerPos(2))

    def generatePlan(self):

        path = []
        

        t = 0
        currentStateDistribution = self.dVectors

        frontier = [State(self.statesList[np.argmax(currentStateDistribution)].getState(), None)]
        frontierValues = [self.cVectors[0]]
        frontierStateDistribution = [currentStateDistribution]
        
        lastState, masterDistribution = self.getBestFromFrontier(frontier, frontierValues, frontierStateDistribution)

        while not lastState.equals(self.goal.getState()):
            #print(self.gVectors[np.argmax(currentStateDistribution)])
            #for pi in range(len(self.gVectors[np.argmax(currentStateDistribution)])):
            #print(self.gVectors)
            self.updateCVectors(np.argmax(currentStateDistribution))
            for idx in range(len(self.gVectors)):
                bestPlan = np.argmin(self.gVectors)
                
                currentStateDistribution = np.matmul(masterDistribution, self.bMatrix[bestPlan])
                frontier.append(Move(list(DIRECTIONS.keys())[bestPlan].result,2,lastState))
                frontierValues.append(self.gVectors[bestPlan] + frontier[-1].getPathLen())
                frontierStateDistribution.append(currentStateDistribution)
                self.gVectors[bestPlan] = 1000
                #time.sleep(3)
                #print(DIRECTIONS.keys())
                #print(self.cVectors[np.argmax(currentStateDistribution)])
            lastState, masterDistribution = self.getBestFromFrontier(frontier, frontierValues)
                
        return lastState
    
    def getBestFromFrontier(self, frontier, frontierValues, frontierStateDistribution):
        idx = np.argmax(frontierValues)[0]
        lastState = frontier[idx]
        masterDistribution = frontierStateDistribution[idx]
        del frontier[idx]
        del frontierValues[idx]
        del frontierStateDistribution[idx]
        return lastState, masterDistribution
