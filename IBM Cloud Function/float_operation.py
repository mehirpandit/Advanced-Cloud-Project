
import math
from time import time
import os


def float_operations(n):
    start = time()
    for i in range(0, n):
        sin_i = math.sin(i)
        cos_i = math.cos(i)
        sqrt_i = math.sqrt(i)
    latency = time() - start
    return latency


def main(event):
    n = int(event['n'])
    result = float_operations(n)
    print(result)
   

    CPU_Pct=str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2))

    #print results
    print("CPU Usage = " + CPU_Pct)
    return { 'message': result }






