import os
import time
import sys

def mem_stress(x):

    set_time = int(x)#3#os.environ['STRESS_MINS']
    timeout = time.time() + 60*float(set_time)  # X minutes from now
    i = 0
    s = '' 
    while True:
        if time.time() > timeout:
            break
        bytearray(i*(10**6))
        time.sleep(1)
        i += 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
       x = int(sys.argv[1])
    else:
       x = 3
    mem_stress(x)
