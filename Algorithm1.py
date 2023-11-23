import sys

#input.txt format:
#node demand
#node demand
#...
#from to weight capacity
#from to weight capacity
#...
#------

class Graph:
    n = 0
    dem = []
    U = []
    C = []
    adj = []
    residual = []


def fileInput(fileName, g):
    file = open(fileName)

    g.n = 0

    for line in file:
        if (len(line) == 0): return
        data = [int(st) for st in line.split()]

        if (len(data) == 1):
            #FIRST LINE
            g.n = data[0] + 2 #for super nodes
            g.dem = [0 for i in range(g.n)]
            g.adj = [[] for i in range(g.n)]
            g.U = g.C = g.residual = [[0 for i in range(g.n)] for j in range(g.n)]
        elif (len(data) == 2):
            #Node and demand
            g.dem[data[0]] = data[1]
        else:
            #Edge
            i = data[0]; j = data[1]; c = data[2]; u = data[3]
            g.U[i][j] = u; g.C[i][j] = c
            g.adj[i].append(j)
            g.adj[j].append(i)
    
def AddSuperNodes(g: Graph):
    g.n += 2


def MinCostFlow(g: Graph):
    g1 = g

    AddSuperNodes(g1)

def main():
    g = Graph()
    fileInput(sys.argv[1], g)

    print(MinCostFlow(g))
    

if __name__ == "__main__":
    main()