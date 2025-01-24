from bfs import BFS
from dfs import DFS
from greedy import Greedy
from state import *
from aStar import *
from maps import *
from heuristics import *
from activeInferenceDecisionMaking import ActiveInference
from activeInferencePlanning import ActiveInferenceV2
import time
import numpy as np

map = MAP1

initialState = State(map[0])

goalState = State(map[1])

heuristic = ManhattanDistance()

###################################################

start_time_a_star = time.time()

search = AStar(initialState, goalState, heuristic)

last = search.search()

end_time_a_star = time.time()

path = []

parent = last
while parent != None:
    path.append(parent)
    #print(parent.getPlayerPos(2))
    parent = parent.getParent()

print("Path of length", len(path)-1, "found with AStar with a time of", end_time_a_star - start_time_a_star)

###################################################

start_time_greedy = time.time()

search = Greedy(initialState, goalState, heuristic)

last = search.search()

end_time_greedy = time.time()

path = []

parent = last
while parent != None:
    path.append(parent)
    #print(parent.getPlayerPos(2))
    parent = parent.getParent()

print("Path of length", len(path)-1, "found with Greedy with a time of", end_time_greedy - start_time_greedy)

###################################################

start_time_act_inf = time.time()


agent = ActiveInference(initialState, goalState, heuristic)

start_time_act_inf_search = time.time()

path = agent.generatePlan()

end_time_act_inf_search = time.time()

end_time_act_inf = time.time()

print("Path of length", len(path), "found with Active Inference with a time of", end_time_act_inf - start_time_act_inf, "the search lasted",end_time_act_inf_search - start_time_act_inf_search)

#print("The path is ", path)
#for elem in path:
#    print(np.array(elem.getState()))
#    time.sleep(2)

#print(end_time_a_star - start_time_a_star , "VS", end_time_act_inf - start_time_act_inf)

###################################################

start_time_act_inf = time.time()

agent = ActiveInferenceV2(initialState, goalState, heuristic)

start_time_act_inf_search = time.time()

path = agent.generatePlan()

end_time_act_inf_search = time.time()

end_time_act_inf = time.time()

print("Path of length", path.getPathLen(), "found with Active Inference V2 with a time of", end_time_act_inf - start_time_act_inf, "the search lasted",end_time_act_inf_search - start_time_act_inf_search)
#print("The path is ", path)
#print(end_time_a_star - start_time_a_star , "VS", end_time_act_inf - start_time_act_inf)

###################################################

start_time_dfs = time.time()

search = DFS(initialState, goalState, heuristic)

last = search.search()

path = []

parent = last
while parent != None:
    path.append(parent)
    #print(parent.getPlayerPos(2))
    parent = parent.getParent()

end_time_dfs = time.time()

print("Path of length", len(path)-1, "found with Depth First Search with a time of", end_time_dfs - start_time_dfs)

###################################################

start_time_bfs = time.time()

search = BFS(initialState, goalState, heuristic)

last = search.search()

path = []

parent = last
while parent != None:
    path.append(parent)
    #print(parent.getPlayerPos(2))
    parent = parent.getParent()

end_time_bfs = time.time()

print("Path of length", len(path)-1, "found with Breath First Search with a time of", end_time_bfs - start_time_bfs)

###################################################