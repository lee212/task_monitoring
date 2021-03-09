import os
import time
import sys

def cpu_stress(x):

    set_time = int(x)#3#os.environ['STRESS_MINS']
    timeout = time.time() + 60*float(set_time)  # X minutes from now
    while True:
        if time.time() > timeout:
            break
        x*x

if __name__ == "__main__":
    if len(sys.argv) > 1:
       x = int(sys.argv[1])
    else:
       x = 3
    cpu_stress(x)
