from actions import *
from heuristics import ManhattanDistance
from maps import *
from state import State
import numpy as np
from utility import OrderedSet

map = MAP2

initialState = State(map[0])

goalState = State(map[1])

heuristic = ManhattanDistance()

ord = OrderedSet()

ord.add(initialState, heuristic.evaluate(initialState, goalState))

print(ord.values)

ord.retrieve()

print(ord.values)

nState = Move("N", 2, initialState).result
wState = Move("W", 2, initialState).result

ord.add(nState, heuristic.evaluate(nState, goalState))
print(ord.values)

ord.add(wState, heuristic.evaluate(wState, goalState))
print(ord.values)

print("nState", ord.retrieve().getPlayerPos(2))

print(ord.values)

currentState = State(nState.getState())

nState = Move("N", 2, currentState).result
eState = Move("E", 2, currentState).result

ord.add(nState, heuristic.evaluate(nState, goalState))
print(ord.values)

ord.add(eState, heuristic.evaluate(eState, goalState))
print(ord.values)


    