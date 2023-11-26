import sys
import heapq
#input.txt format:
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

    while queue:
        u, d = heapq.heappop(queue)
        visited[u] = True
        print(u)
        #Found path to  sink
        if (u == g.numOfNodes-1): break

        print("Adj to: ")
        for v in range(g.numOfNodes):
            #      edge exists              flow can increase
            if (u, v) in g.capacity and g.capacity[(u, v)] - g.flow[(u, v)] > 0 and not visited[v]:
                print(v)
                reduced_cost = g.cost[(u, v)] + g.demand[v] - g.demand[u]
                print("Distance cmp: ", distance[v], " and ", distance[u] + reduced_cost)
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

                rg.flow[(i, j)] = g.flow[(i, j)]
                if g.flow[(i, j)] > 0:
                    #Has reversed edge
                    rg.capacity[(j, i)] = g.flow[(i, j)]
                    rg.flow[(j, i)] = g.flow[(i, j)]
                    rg.cost[(j, i)] = -g.cost[(i, j)]
    return rg

def MinCostFlow(g: Graph):
    AddSuperNodes(g)

    cnt = 0

    while True:
        rg  = BuildResidualGraph(g)

        print(rg.cost)
        print(rg.capacity)
        print(rg.flow)

        distance, predecessor = ShortestPath(rg)
        print(distance)
        print(predecessor)
        
        cnt += 1
        if cnt == 1: break


def main():
    g = Graph()
    fileInput(sys.argv[1], g)

    print(MinCostFlow(g))
    

if __name__ == "__main__":
    main()