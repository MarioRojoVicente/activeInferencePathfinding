
###################################################

import time

from activeInferencePlanning import ActiveInferenceV2
from heuristics import ManhattanDistance
from maps import *
from state import State

map = MAP1

initialState = State(map[0])

goalState = State(map[1])

heuristic = ManhattanDistance()

start_time_act_inf = time.time()

agent = ActiveInferenceV2(initialState, goalState, heuristic)

start_time_act_inf_search = time.time()

path = agent.generatePlan()

end_time_act_inf_search = time.time()

end_time_act_inf = time.time()

print("Path of length", len(path), "found with Active Inference V2 with a time of", end_time_act_inf - start_time_act_inf, "the search lasted",end_time_act_inf_search - start_time_act_inf_search)
#print("The path is ", path)
#print(end_time_a_star - start_time_a_star , "VS", end_time_act_inf - start_time_act_inf)

###################################################