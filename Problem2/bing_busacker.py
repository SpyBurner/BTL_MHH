# Import the heapq module to use a priority queue
import heapq

# Define a function to read the input from the file
def read_input(filename):
    # Open the file for reading
    with open(filename, "r") as f:
        # Read the first line to get the number of nodes
        numOfNodes = int(f.readline())
        # Initialize the demand, cost, capacity, and flow dictionaries
        demand = {}
        cost = {}
        capacity = {}
        flow = {}
        # Loop through the next numOfNodes lines to get the demand of each node
        for i in range(numOfNodes):
            # Split the line by space and get the node and the demand
            node, d = map(int, f.readline().split())
            # Store the demand in the dictionary
            demand[node] = d
        # Loop through the remaining lines to get the edges and their attributes
        for line in f:
            # Split the line by space and get the nodes, the weight, and the capacity
            u, v, w, c = map(int, line.split())
            # Store the cost, the capacity, and the flow in the dictionaries
            cost[(u, v)] = w
            capacity[(u, v)] = c
            flow[(u, v)] = 0
    # Return the number of nodes and the dictionaries
    return numOfNodes, demand, cost, capacity, flow

# Define a function to find the shortest path from the source to the sink in the residual network
def shortest_path(numOfNodes, demand, cost, capacity, flow):
    # Initialize the distance, the predecessor, and the visited dictionaries
    distance = {}
    predecessor = {}
    visited = {}
    # Loop through all the nodes and set the distance to infinity, the predecessor to None, and the visited to False
    for i in range(numOfNodes):
        distance[i] = float("inf")
        predecessor[i] = None
        visited[i] = False
    # Set the distance of the source to zero
    distance[0] = 0
    # Create an empty priority queue
    queue = []
    # Push the source node and its distance to the queue
    heapq.heappush(queue, (0, 0))
    # Loop until the queue is empty
    while queue:
        # Pop the node with the minimum distance from the queue
        d, u = heapq.heappop(queue)
        # Mark the node as visited
        visited[u] = True
        # If the node is the sink, break the loop
        if u == numOfNodes - 1:
            break
        # Loop through all the adjacent nodes of the current node
        for v in range(numOfNodes):
            # If the edge from u to v has positive residual capacity and the node v is not visited
            if (u, v) in capacity and capacity[(u, v)] - flow[(u, v)] > 0 and not visited[v]:
                # Calculate the reduced cost of the edge
                reduced_cost = cost[(u, v)] + demand[u] - demand[v]
                # If the distance of v can be improved by relaxing the edge
                if distance[v] > distance[u] + reduced_cost:
                    # Update the distance and the predecessor of v
                    distance[v] = distance[u] + reduced_cost
                    predecessor[v] = u
                    # Push the node v and its distance to the queue
                    heapq.heappush(queue, (distance[v], v))
    # Return the distance and the predecessor dictionaries
    return distance, predecessor

# Define a function to augment the flow along the shortest path and update the potentials
def augment_flow(numOfNodes, demand, cost, capacity, flow, distance, predecessor):
    # Initialize the residual capacity of the path to infinity
    residual_capacity = float("inf")
    # Initialize the current node to the sink
    v = numOfNodes - 1
    # Loop until the current node is the source
    while v != 0:
        # Get the predecessor of the current node
        u = predecessor[v]
        # Update the residual capacity of the path by taking the minimum of the current value and the residual capacity of the edge
        residual_capacity = min(residual_capacity, capacity[(u, v)] - flow[(u, v)])
        # Update the current node to the predecessor
        v = u
    # Initialize the current node to the sink
    v = numOfNodes - 1
    # Loop until the current node is the source
    while v != 0:
        # Get the predecessor of the current node
        u = predecessor[v]
        # Update the flow of the edge by adding the residual capacity of the path
        flow[(u, v)] += residual_capacity
        # Update the flow of the reverse edge by subtracting the residual capacity of the path
        flow[(v, u)] -= residual_capacity
        # Update the current node to the predecessor
        v = u
    # Loop through all the nodes
    for i in range(numOfNodes):
        # Update the potential of the node by adding the distance of the node
        demand[i] += distance[i]

# Define a function to solve the minimum-cost flow problem using the successive shortest path algorithm
def min_cost_flow(filename):
    # Read the input from the file
    numOfNodes, demand, cost, capacity, flow = read_input(filename)
    # Loop until there is no more augmenting path
    while True:
        # Find the shortest path from the source to the sink in the residual network
        distance, predecessor = shortest_path(numOfNodes, demand, cost, capacity, flow)
        # If the distance of the sink is infinity, break the loop
        if distance[numOfNodes - 1] == float("inf"):
            break
        # Augment the flow along the shortest path and update the potentials
        augment_flow(numOfNodes, demand, cost, capacity, flow, distance, predecessor)
    # Return the flow dictionary
    return flow

# Define a function to print the flow and the total cost
def print_result(flow, cost):
    # Initialize the total cost to zero
    total_cost = 0
    # Loop through all the edges in the flow dictionary
    for edge in flow:
        # Get the nodes, the flow, and the cost of the edge
        u, v = edge
        f = flow[edge]
        c = cost[edge]
        # Print the edge and the flow
        print(f"Edge ({u}, {v}): Flow = {f}")
        # Update the total cost by adding the product of the flow and the cost
        total_cost += f * c
    # Print the total cost
    print(f"Total cost = {total_cost}")

# Call the main function to solve the problem and print the result
if __name__ == "__main__":
    # Solve the problem and get the flow
    flow = min_cost_flow("input.txt")
    # Print the flow and the total cost
    print_result(flow, cost)
