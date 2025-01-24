from actions import *
from heuristics import Heuristic
from utility import OrderedSet, Set

class AStar():

    def __init__(self, start:State, goal:State, h:Heuristic):
        self.h = h
        self.goal = goal
        self.frontier = OrderedSet() #ordered set
        self.frontier.add(start, self.evaluate(start))
        self.visited = Set() #unordered set

    def search(self):
        t = 0
        while not self.frontier.isEmpty():
            curentState = self.frontier.retrieve()
            self.visited.add(curentState)
            if curentState.equals(self.goal.getState()):
                print("AStar did", t, "iterations.")
                return curentState
            else:
                children = self.getChildren(curentState)
                for child in children:
                    if not self.visited.checkElement(child.getState()):
                        #print("Not Visited")
                        self.frontier.add(child, self.evaluate(child))
                    #print("Visited")
            t += 1
        
        raise Exception ("Frontier is empty. Path was not found.")
            

    def getChildren(self, current):
        children = []
        for dir in DIRECTIONS.keys():
            child = Move(dir, 2, current).result
            if child != -1:#if move is valid
                children.append(child)
        return children
            

    def evaluate(self, child):
        return child.getPathLen() + self.h.evaluate(child, self.goal)
    

