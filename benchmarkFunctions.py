import decimal
from decimal import Decimal
import time
###TIME
# Define a global variable to store the starting time
decimal.getcontext().prec = 60
start_time = Decimal(0.0)
# Define a function to set the starting time
def set_start_time():
    global start_time
    start_time = Decimal(time.time())
    # print("Starting time set to", start_time)
# Define a function to output the elapsed time
def get_elapsed_time():
    global start_time
    if start_time is None:
        print("Please set the starting time first")
    else:
        elapsed_time = Decimal(Decimal(time.time()) - start_time)
        print("Elapsed time is", format(elapsed_time, ".20f"), "seconds")
###
