import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism


# Define the ai function based on Corollary 4.4
def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)

# Define the modified binary mechanism as an unbounded function
def binary_mechanism_unbounded(epsilon, stream, alpha_hat, t_last, theta=1):
    # Initialize alphas dynamically
    alpha = []
    B = []

    
    for t in range(t_last, t_last+len(stream)):
        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Extend the alpha arrays if needed
        if len(alpha) < num_bits:
            alpha.extend([0] * (num_bits - len(alpha)))
            alpha_hat.extend([0] * (num_bits - len(alpha_hat)))

        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Reset previous values to 0
        for j in range(i):
            alpha[j] = 0
            alpha_hat[j] = 0

        # Add Laplacian noise to alpha_hat_i
        alpha_hat[i] = alpha[i] + laplace_mechanism(ai(i, theta)/epsilon)
        
        # Sum for output and append to B
        B.append(sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1))

        t_newlast = t
    
    return B, alpha_hat, t_newlast+1
