import sys

#input.txt format:
#node demand
#node demand
#...
#from to weight capacity
#from to weight capacity
#...
#------

dem, U, C, adj = []
residual = []

def fileInput(fileName):
    file = open(fileName)

    n = 0


    for line in file:
        if (len(line) == 0): return

        data = [int(st) for st in line.split()]

        if (len(data) == 1):
            #FIRST LINE
            n = data[0]
            dem = [0 for i in range(n)]
            adj = [[] for i in range(n)]
            U = C = residual = [[0 for i in range(n)] for j in range(n)]
        elif (len(data) == 2):
            #Node and demand
            dem[data[0]] = data[1]
        else:
            #Edge
            i = data[0]; j = data[1]; c = data[2]; u = data[3]
            U[i][j] = u; C[i][j] = c
            adj[i].append(j)

    

def main():
    fileInput(sys.argv[1])


if __name__ == "__main__":
    main()