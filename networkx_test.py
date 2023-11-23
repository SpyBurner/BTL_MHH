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

#need fixing
def fileInput(fileName):
    file = open(fileName)
    for line in file:
        #EOF/error
        if (len(line) == 0): break

        #Get data from line
        data = [int(st) for st in line.split()]

        if (len(data) == 2):
            if (line.index == 0):
                nodeCnt = data[0]
                carCnt = data[1]
            else:
                G.add_node(data[0], demand=data[1])
        else:
            G.add_edge(data[0], data[1], weight=data[2], capacity=data[3])
    

def main():
    G = nx.DiGraph()

    G.add_node("a", demand=-5)
    G.add_node("d", demand=5)

    G.add_edge("a", "b", weight=3, capacity=4)
    G.add_edge("a", "c", weight=6, capacity=10)
    G.add_edge("b", "d", weight=1, capacity=9)
    G.add_edge("c", "d", weight=2, capacity=5)

    # flowCost, flowDict = nx.capacity_scaling(G)
    # print(flowCost)
    # print(flowDict)

    print(nx.adjacency_matrix(G))
    
if __name__ == "__main__":
    main()
