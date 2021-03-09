import os
import time
import sys
import torch

def gpu_stress(x):

    set_time = int(x)#3#os.environ['STRESS_MINS']
    timeout = time.time() + 60*float(set_time)  # X minutes from now
    i = 0
    x = torch.linspace(0, 4, 16*1024**2).cuda() # take device index, or CUDA_VISIBLE_DEVICES
    while True:
        if time.time() > timeout:
            break
        x = x * (1.0 - x)
        time.sleep(1)
        i += 1

if __name__ == "__main__":
    if len(sys.argv) > 1:
       x = int(sys.argv[1])
    else:
       x = 3
    gpu_stress(x)
