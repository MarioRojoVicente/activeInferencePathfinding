import copy 

class State():
    def __init__(self, map, parent=None):
        self.map = map
        self.parent = parent
        if parent != None:
            self.pathLength = parent.getPathLen() + 1
        else:
            self.pathLength = 0

    def equals(self, element):
        """for row in self.map:
            print(row)
        print("XXXXXXXXXXXXXXXXXXX")
        for row in element:
            print(row)"""
        for rowIdx in range(0,len(self.map)):
            for colIdx in range(0,len(self.map[0])):
                if element[rowIdx][colIdx] != self.map[rowIdx][colIdx]:
                    #print("False")
                    return False
        #print("True")
        return True
    
    def getState(self):
        return copy.deepcopy(self.map)
    
    def getParent(self):
        return self.parent
    
    def getPathLen(self):
        return self.pathLength
    
    def getPlayerPos(self, player):
        for rowIdx in range(0,len(self.map)):
            for colIdx in range(0,len(self.map[0])):
                if self.map[rowIdx][colIdx] == player:
                    return [rowIdx, colIdx]
        raise Exception("Player", player, "not in state.")
