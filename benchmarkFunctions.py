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