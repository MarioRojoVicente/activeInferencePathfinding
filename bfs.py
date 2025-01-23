from actions import *
from heuristics import Heuristic
from utility import OrderedSet, Set

class BFS():
    
    def __init__(self, start:State, goal:State, h:Heuristic):
            self.h = h
            self.goal = goal
            self.frontier = [] #ordered set
            self.frontier.append(start)
            self.visited = Set() #unordered set

    def search(self):
        while not len(self.frontier)==0:
            curentState = self.frontier[0]
            self.frontier = self.frontier[1:]
            self.visited.add(curentState)
            if curentState.equals(self.goal.getState()):
                return curentState
            else:
                children = self.getChildren(curentState)
                for child in children:
                    if not self.visited.checkElement(child.getState()):
                        #print("Not Visited")
                        self.frontier.append(child)
                    #print("Visited")

        raise Exception ("Frontier is empty. Path was not found.")
            

    def getChildren(self, current):
        children = []
        for dir in DIRECTIONS.keys():
            child = Move(dir, 2, current).result
            if child != -1:#if move is valid
                children.append(child)
        return children