import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism

# Function that implements the two level mechanism
def two_level_mechanism(T, epsilon, sigma, B):

    # Initialize alpha and beta
    alpha = np.zeros(T)
    beta = np.zeros(T // B + (T % B > 0))  # this is one longer than need to be. 
    
    # Loops through each time step in the stream
    for t in range(1, T + 1):
        alpha[t-1] = laplace_mechanism(sigma[t-1], 1, epsilon)
        q, r = divmod(t, B)
        if r == 0:  # Check if t is at the end of a bucket
            beta[q-1] = laplace_mechanism(sum(sigma[t-B+1:t]), 1, epsilon)
        
        # Calculate D(t)
        D_t = sum(beta[:q]) + sum(alpha[q*B+1:t])
        # Output estimate at every time step
        yield D_t
