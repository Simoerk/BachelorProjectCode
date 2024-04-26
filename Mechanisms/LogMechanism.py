import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism

# Unused
def logarithmic_mechanism(epsilon, stream):
    # Initialize beta
    beta = 0
    
    # Output estimate at each power of two time step
    output = {}

    for t, value in enumerate(stream, start=1):
        beta += value
        if math.log2(t).is_integer():  # Check if t is a power of 2
            beta += laplace_mechanism(1,epsilon)
            output[t] = beta
    
    return output