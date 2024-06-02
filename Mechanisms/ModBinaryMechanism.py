import math
from utils.laplace import *

# Function that implements the modified binary mechanism as an unbounded mechanism
def mod_binary_mechanism(epsilon, stream, theta):
    # Initialize alphas
    alpha = []
    B = []
    alpha_hat = []

    t_last = 1
    # Loops through each time step
    for t in range(t_last, t_last+len(stream)):

        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Extend the alpha arrays if needed
        if len(alpha) < num_bits:
            alpha.extend([0] * (num_bits - len(alpha)))
            alpha_hat.extend([0] * (num_bits - len(alpha_hat)))

        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
        bin_t.reverse() # bin_t was reversed
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Set unused alpha values to 0
        for j in range(i):
            alpha[j] = 0
            alpha_hat[j] = 0

        # Add Laplacian noise to alpha_hat_i with the ai function in laplace
        alpha_hat[i] = laplace_mechanism(alpha[i], ai(i, theta), epsilon)
        
        # Sum for output and append to B
        B.append(sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1))
         
    return B
