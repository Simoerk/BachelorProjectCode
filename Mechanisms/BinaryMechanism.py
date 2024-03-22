import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism


def binary_mechanism(T, epsilon, stream):
    # Initialize alphas
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    
    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log(T))
    
    # Output estimate at each time step
    B = [0] * T
    
    for t in range(1, T + 1):
        # Convert t to binary form
        bin_t = [int(x) for x in bin(t)[2:]]

        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t  # Pad with zeros to match alpha length

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Overwrite previous values with 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Add Laplacian noise to alpha_hat_i
        alpha_hat[i] = alpha[i] + laplace_mechanism(1/epsilon_prime)
        
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    return B

