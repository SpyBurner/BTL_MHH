import sys
import networkx as nx

import benchmarkFunctions as bf
#Read from file
def fileInput(fileName, G: nx.DiGraph):
    file = open(fileName, "r")

    n = 0

    demand = {}

    for line in file:
        if (len(line) == 0): return
        data = [int(st) for st in line.split()]

        if (len(data) == 1):
            n = data[0]
            G.add_nodes_from([i for i in range(1, n+1)])
            for i in range(1, n+1):
                demand[i] = 0

        elif (len(data) == 2):
            #Node and demand
            u, d = data
            demand[u] = d

        else:
            #Edge
            i, j, c, u = data
            G.add_edge(i, j, cost=c, capacity=u)
    nx.set_node_attributes(G, demand, "demand")

def main():
    G = nx.DiGraph()

    fileInput(sys.argv[1], G)

    # print(nx.get_node_attributes(G, "demand"))
    print("Networkx solver:")
    print("Network simplex:")
    bf.set_start_time()
    flowCost, flowDict = nx.network_simplex(G, weight="cost", capacity="capacity")
    bf.get_elapsed_time()

    print("Capacity scaling:")
    bf.set_start_time()
    flowCost, flowDict = nx.capacity_scaling(G, weight="cost", capacity="capacity")
    bf.get_elapsed_time()

    print("Result: ", flowCost)
    # print(flowDict)

    
if __name__ == "__main__":
    main()
