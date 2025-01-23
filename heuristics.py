from actions import DIRECTIONS, Move

class Heuristic():

    def __init__(self):
        pass

    def evaluate(self, origin, goal):
        return -1
    
class ManhattanDistance(Heuristic):

    def __init__(self):
        pass

    def evaluate(self, origin, goal):
        origin_pos = origin.getPlayerPos(2)
        goal_pos = goal.getPlayerPos(2)
        return abs(goal_pos[0]-origin_pos[0]) + abs(goal_pos[1]-origin_pos[1])
    
class TrueDistance(Heuristic):
    def __init__(self, goal):
        frontier = [goal]
        visitedStates = []
        distances = []
        while len(frontier) > 0:
            current = frontier[0]
            frontier = frontier[1:]
            visitedStates.append(current)
            dist = 0
            parent = current.getParent()
            while parent != None:
                dist += 1
                parent = parent.getParent()
            distances.append(dist)
            for dir in DIRECTIONS:
                newState = Move(dir, 2, current).result
                if newState != -1:
                    visited = False
                    for elem in visitedStates:
                        if elem.equals(newState.getState()):
                            visited = True
                            break
                    if not visited:
                        frontier.append(newState)
        self.stateList = visitedStates
        self.stateEvals = distances

    def evaluate(self, origin, goal):
        for stateIdx in range(len(self.stateList)):
            if self.stateList[stateIdx].equals(origin.getState()):
                return self.stateEvals[stateIdx]
        raise Exception("Invalid state for evaluation.")