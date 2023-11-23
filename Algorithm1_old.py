import sys

#input.txt format:
#node demand
#node demand
#...
#from to weight capacity
#from to weight capacity
#...
#------

def fileInput(fileName):
    file = open(fileName)
    for line in file:
        if (len(line) == 0): return

        data = [int(st) for st in line.split()]

        if (len(line) == 2):
            
    

def main():
    adj, demand = fileInput(sys.argv[1])


if __name__ == "__main__":
    main()