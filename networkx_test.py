import networkx as nx

import time
###TIME
# Define a global variable to store the starting time
start_time = None
# Define a function to set the starting time
def set_start_time():
    global start_time
    start_time = time.time()
    print("Starting time set to", start_time)
# Define a function to output the elapsed time
def get_elapsed_time():
    global start_time
    if start_time is None:
        print("Please set the starting time first")
    else:
        elapsed_time = time.time() - start_time
        print("Elapsed time is", elapsed_time, "seconds")
###

G = nx.DiGraph()

G.add_node("a", demand=-5)
G.add_node("d", demand=5)

G.add_edge("a", "b", weight=3, capacity=4)
G.add_edge("a", "c", weight=6, capacity=10)
G.add_edge("b", "d", weight=1, capacity=9)
G.add_edge("c", "d", weight=2, capacity=5)

flowCost, flowDict = nx.capacity_scaling(G)
print(flowCost)
print(flowDict)