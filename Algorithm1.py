import sys
import heapq

import matplotlib.pyplot as plt
import networkx as nx

import benchmarkFunctions as bf

#input .txt format:
#numOfNodes
#node demand
#node demand
#...
#from to weight capacity
#from to weight capacity
#...
#------

class Graph:
    def __init__(self):
        self.numOfNodes = 0
        self.demand = {}
        self.cost = {}
        self.capacity = {}
        self.flow = {}

    def printData(self):
        print("Number of nodes:")
        print(self.numOfNodes)
        print("Demand of each node:")
        for node in self.demand:
            print(f"Node {node}: Demand = {self.demand[node]}")
        print("Cost of each edge:")
        for edge in self.cost:
            u, v = edge
            print(f"Edge ({u}, {v}): Cost = {self.cost[edge]}")
        print("Capacity of each edge:")
        for edge in self.capacity:
            u, v = edge
            print(f"Edge ({u}, {v}): Capacity = {self.capacity[edge]}")
        print("Flow of each edge:")
        for edge in self.flow:
            u, v = edge
            print(f"Edge ({u}, {v}): Flow = {self.flow[edge]}")


def fileInput(fileName, g : Graph):
    file = open(fileName, "r")

    for line in file:
        if (len(line) == 0): return
        data = [int(st) for st in line.split()]

        if (len(data) == 1):
            #FIRST LINE
            g.numOfNodes = data[0]

            for i in range(g.numOfNodes):
                g.demand[i] = 0
        elif (len(data) == 2):
            #Node and demand
            g.demand[data[0]] = data[1]
        else:
            #Edge
            i, j, c, u = data
            g.cost[(i, j)] = c
            g.capacity[(i, j)] = u
            g.flow[(i, j)] = 0

#Assume node indexes start from 1
#0 as source, n+1 as sink
def AddSuperNodes(g: Graph):
    n = g.numOfNodes

    g.demand[0] = 0
    g.demand[n + 1] = 0

    for i in range(1, n+1):
        if (g.demand[i] < 0):
            g.cost[(0, i)] = 0
            g.capacity[(0, i)] = abs(g.demand[i])
            g.flow[(0, i)] = 0

            g.demand[0] += g.demand[i]
        elif (g.demand[i] > 0):
            g.cost[(i, n + 1)] = 0
            g.capacity[(i, n + 1)] = abs(g.demand[i])
            g.flow[(i, n + 1)] = 0
        
            g.demand[n + 1] += g.demand[i]
        g.demand[i] = 0
    
    #to add 2 new nodes
    g.numOfNodes+= 2

def ShortestPath(g: Graph):
    #LABEL-CORRECTING / Dijkstra
    distance = {} #Distance from source to node i
    predecessor = {} #Trace/previous node of i
    visited = {}

    #Init
    for i in range(g.numOfNodes):
        distance[i] = float("inf")
        predecessor[i] = None
        visited[i] = False

    #starting distance of source
    distance[0] = 0
    #priority queue
    queue = []
    #tuple: (distance, node)
    #python heap sorts by first of tuple
    heapq.heappush(queue, (0,0))

    while len(queue):
        d, u = heapq.heappop(queue)
        if visited[u]: continue
        visited[u] = True
        #Found path to  sink
        if (u == g.numOfNodes-1): break
        for v in range(g.numOfNodes):
            #      edge exists              flow can increase
            if (u, v) in g.capacity and g.capacity[(u, v)] - g.flow[(u, v)] > 0 and not visited[v]:
                reduced_cost = g.cost[(u, v)] + g.demand[v] - g.demand[u]
                if (distance[v] > distance[u] + reduced_cost):
                    distance[v] = distance[u] + reduced_cost
                    predecessor[v] = u
                    heapq.heappush(queue, (distance[v], v))
    return distance, predecessor

def BuildResidualGraph(g: Graph):
    rg = Graph()

    rg.numOfNodes = g.numOfNodes

    for i in range(g.numOfNodes):
        for j in range(g.numOfNodes):
            if (i, j) in g.capacity:
                rg.capacity[(i, j)] = g.capacity[(i, j)]
                rg.cost[(i, j)] = g.cost[(i, j)]
                rg.demand[i] = g.demand[i]
                rg.demand[j] = g.demand[j]

                rg.flow[(i, j)] = g.flow[(i, j)]
                if g.flow[(i, j)] > 0:
                    #Has reversed edge
                    rg.capacity[(j, i)] = g.flow[(i, j)]
                    rg.flow[(j, i)] = g.flow[(i, j)]
                    rg.cost[(j, i)] = -g.cost[(i, j)]
    return rg

def AugmentFlow(g: Graph, predecessor):
    #The amount of flow unit to incr along path
    residual_capacity = float("inf")
    
    v = g.numOfNodes - 1
    #going backward on the path to find min residual_capacity
    while v != 0 and predecessor[v] != None:
        u = predecessor[v]
        residual_capacity = min(residual_capacity, g.capacity[(u, v)] - g.flow[(u, v)])
        v = u
    
    v = g.numOfNodes - 1
    #going backward again to incr
    while v != 0 and predecessor[v] != None:
        u = predecessor[v]
        g.flow[(u, v)] += residual_capacity

        if (v == g.numOfNodes - 1): g.demand[v] -= residual_capacity

        v = u
    g.demand[0] += residual_capacity

def CalculateCost(g: Graph):
    totalCost = 0

    for e in g.flow:
        totalCost += g.flow[e] * g.cost[e]
    return totalCost

def MinCostFlow(g: Graph):
    AddSuperNodes(g)
    GraphPlot(g)
    while True:
        rg  = BuildResidualGraph(g)
        distance, predecessor = ShortestPath(rg)        
        AugmentFlow(g, predecessor)
        if (distance[g.numOfNodes-1] == float("inf")): break
    return CalculateCost(g)

#Only use for flow with source = 0
def GraphPlot(g: Graph):
    return
    G = nx.DiGraph()
    pos = {}

    visited = {}
    queue = []
    #node, level
    queue.append((0, 1))

    level = {}

    while (queue):
        u, l = queue.pop()
        if (u in visited): continue
        visited[u] = True
        
        if (not l in level): level[l] = 1
        else: level[l] += 1
        pos[u] = (l + 10, level[l]/5)

        for v in range(g.numOfNodes):
            if (u, v) in g.capacity:
                queue.append((v, l + 1))
                G.add_edge(u, v, capacity=g.capacity[(u, v)], flow=g.flow[(u, v)], cost=g.cost[(u, v)])
    nx.draw_networkx(G, pos=pos, node_size = 500)

    label1 = g.flow
    label2 = g.capacity
    label3 = g.cost

    labelFinal = {}
    for e in label1:
        labelFinal[e] = (label3[e], (label1[e], label2[e]))

    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = labelFinal)

    plot1 = plt.subplot()
    plt.axis("off")
    plt.show()

def main():
    g = Graph()
    fileInput(sys.argv[1], g)
    print("Algorithm 1")

    bf.set_start_time()
    res = MinCostFlow(g)
    bf.get_elapsed_time()

    print("Result: ", res)
    GraphPlot(g)

if __name__ == "__main__":
    main()