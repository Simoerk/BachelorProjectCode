import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism


def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)

def binary_mechanism_modified(T, epsilon, stream):
    # Ensure theta > 0 as per Corollary 4.4
    theta = 1
    
    # Initialize alphas
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    
    # Output estimate at each time step
    B = [0] * T
    
    for t in range(1, T + 1):
        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(len(alpha))]
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Reset previous values to 0
        for j in range(i):
            alpha[j] = 0
            alpha_hat[j] = 0

        # Calculate epsilon_prime based on the modified strategy for ai
        epsilon_prime = epsilon / math.log(T) * ai(i, theta)
        
        # Add Laplacian noise to alpha_hat_i
        alpha_hat[i] = alpha[i] + laplace_mechanism(1/epsilon_prime)
        
        # Sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    
    return B
