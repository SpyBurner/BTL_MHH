import sys
import heapq

import matplotlib.pyplot as plt
import networkx as nx

import benchmarkFunctions as bf
import random
import math
#node indexes start at 1
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

def CalculatePotentials(g: Graph):
    for i in range(g.numOfNodes):
        g.demand[i] = float('inf')
    
    #Use Ford-Bellman, potentials are treated as the distance to the source of a node
    #Initial potential of source
    g.demand[0] = 0
    #Flag to stop the algo early
    changed = False
    for k in range(g.numOfNodes-1):
        for i in range(g.numOfNodes):
            for j in range(g.numOfNodes):
                #          edge exists        distance from i to j can be lowered
                if (i, j) in g.cost and g.demand[j] > g.demand[i] + g.cost[(i, j)]:
                    g.demand[j] = g.demand[i] + g.cost[(i, j)]
                    changed = True
        if not changed: break
        changed = False

    #Negative cycle check
    changed = False
    for i in range(g.numOfNodes):
            for j in range(g.numOfNodes):
                if ((i, j) in g.cost and g.demand[j] > g.demand[i] + g.cost[(i, j)]):
                    g.demand[j] = g.demand[i] + g.cost[(i, j)]
                    changed = True
    
    #This source code does not solve for networks with negative cost cycles
    if changed: 
        print("Negative cycle detected!")
        exit()

def ShortestPath(rg: Graph):
    #use Dijkstra for performance
    distance = {} #Distance from source to node i
    predecessor = {} #Trace/previous node of i
    visited = {}

    #Init
    for i in range(rg.numOfNodes):
        distance[i] = float("inf")
        predecessor[i] = None
        visited[i] = False

    #starting distance of source
    distance[0] = 0
    #priority queue
    queue = []
    #tuple: (distance, from, to)
    #python heap cmp by first of tuple
    heapq.heappush(queue, (0,0,0))

    while len(queue):
        d, u, v = heapq.heappop(queue)
        if visited[v]: continue
        
        visited[v] = True
        predecessor[v] = u
        if (u, v) in rg.cost:
            print("Reduced cost: ", u, "->", v," = ", rg.cost[(u, v)], " - ", rg.demand[v], " + ", rg.demand[u], "\n = ", reduced_cost)

        #Found greedy path to sink
        if (visited[rg.numOfNodes-1]): break
        
        #Update distances of nodes adjacent to v, using u as v
        u = v
        for v in range(rg.numOfNodes):
            #      edge exists              flow can increase
            if (u, v) in rg.capacity and rg.capacity[(u, v)] - rg.flow[(u, v)] > 0 and not visited[v]:
                reduced_cost = rg.cost[(u, v)] - rg.demand[v] + rg.demand[u]
                if (distance[v] > distance[u] + reduced_cost):
                    distance[v] = distance[u] + reduced_cost
                    heapq.heappush(queue, (distance[v], u, v))
    return distance, predecessor

def AugmentFlow(g: Graph, distance, predecessor):
    #The amount of flow unit to increase along path
    residual_capacity = float("inf")
    
    v = g.numOfNodes - 1
    #going backward on the path to find min residual_capacity
    while v != 0 and predecessor[v] != None:
        u = predecessor[v]
        residual_capacity = min(residual_capacity, g.capacity[(u, v)] - g.flow[(u, v)])
        v = u
    
    v = g.numOfNodes - 1
    g.demand[v] = distance[v]
    #going backward again to increase
    while v != 0 and predecessor[v] != None:
        u = predecessor[v]
        g.flow[(u, v)] += residual_capacity
        
        #new potentials are the length of the path found
        g.demand[u] = g.demand[v] - g.cost[(u, v)]

        v = u

def CalculateCost(g: Graph):
    totalCost = 0

    for e in g.flow:
        totalCost += g.flow[e] * g.cost[e]
    return totalCost

def MinCostFlow(g: Graph):
    AddSuperNodes(g)
    CalculatePotentials(g)
    print(g.demand)
    while True:
        rg  = BuildResidualGraph(g)
        distance, predecessor = ShortestPath(rg)
        #Fails to find a path
        if (distance[g.numOfNodes-1] == float("inf")): break
        AugmentFlow(g, distance, predecessor)
        print(g.demand)
    return CalculateCost(g)

#Only use for flow with source = 0
def GraphPlot(g: Graph):
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
        
        level[u] = l
        # pos[u] = (u, 5*math.cos(random.random()*math.pi))
        pos[u] = (level[u], u)

        for v in range(g.numOfNodes):
            if (u, v) in g.capacity:
                queue.append((v, l + 1))
                G.add_edge(u, v, capacity=g.capacity[(u, v)], flow=g.flow[(u, v)], cost=g.cost[(u, v)])
    alt = -1
    for i in range(g.numOfNodes):
        for j in range(i + 1, g.numOfNodes):
            if pos[i][0] == pos[j][0]:
                while abs(pos[i][1] - pos[j][1]) < 3:
                    pos[j] = (pos[j][0], pos[j][1] + 1)
                pos[j] = (pos[j][0] - 0.1 * alt, pos[j][1])
                alt *= -1
    nx.draw_networkx(G, pos=pos, node_size = 300)


    label1 = g.flow
    label2 = g.capacity
    label3 = g.cost

    labelFinal = {}
    for e in label1:
        labelFinal[e] = (label3[e], (label1[e], label2[e]))

    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels = labelFinal, label_pos=0.6)

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