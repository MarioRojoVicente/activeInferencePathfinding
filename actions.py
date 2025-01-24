from state import *

DIRECTIONS = {"N": [-1,0], "W": [0, -1], "E": [0,1], "S": [1,0], "NM": [0,0]}

class Move():

    def __init__(self, direction, player, state):
        if (direction not in DIRECTIONS.keys()):
            raise Exception(direction, "is not a valid direction. Valid directions are N, W, E, S and NM")
        elif (player not in range(2,9)):
            raise Exception(player, "is not a valid player. Valid players are in range 2 to 9.")
        else:
            self.result = self.move(player, state, state.getState(), DIRECTIONS[direction])

    def move(self, player, state, map, move):
        playerIndex = [0,0]
        for row in range(0, len(map)):
            for col in range(0, len(map)):
                if map[row][col] == player:
                    playerIndex = [row, col]

        if (self.moveIsValid(map, move, playerIndex)):
            map[playerIndex[0]][playerIndex[1]] = 0
            map[playerIndex[0]+move[0]][playerIndex[1]+move[1]] = player
        
            return State(map, state)
        
        else:
            return -1

    def moveIsValid(self, map, move, playerIndex):
        finalTile = map[playerIndex[0]+move[0]][playerIndex[1]+move[1]]
        #print(playerIndex[0]+move[0], playerIndex[1]+move[1], finalTile)
        if finalTile == 1:#Tries to move to a wall
            return False
        else:
            return True
        
        
