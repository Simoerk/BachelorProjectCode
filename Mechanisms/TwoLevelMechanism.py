import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism

def two_level_mechanism(T, epsilon, sigma, B):
    # Initialize alpha and beta
    alpha = np.zeros(T)
    beta = np.zeros(T // B + (T % B > 0))  
    
    # Mechanism
    for t in range(1, T + 1):
        lap = laplace_mechanism(1,epsilon)
        alpha[t-1] = sigma[t-1] + lap
        q, r = divmod(t, B)
        if r == 0:  # Check if t is at the end of a bucket
            #print("t: " , t)
            lap = laplace_mechanism(1,epsilon)
            beta[q-1] = sum(sigma[t-B+1:t]) + lap
        
        # Calculate D(t)
        D_t = sum(beta[:q]) + sum(alpha[q*B+1:t])
        yield D_t
