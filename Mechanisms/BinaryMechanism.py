import math
from utils.laplace import laplace_mechanism

# Function that implements the binary mechanism
def binary_mechanism(T, epsilon, stream):
    # Initialize alphas
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    
    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log2(T))
    
    # Output estimate at each time step
    B = [0] * T
    
    # Loop through each time step in stream
    for t in range(1, T + 1):
        # Convert t to binary form
        bin_t = [int(x) for x in bin(t)[2:]]

        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t  # Pad with zeros to match alpha length

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse() # bin_t was in reverse order
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Set unused alpha values to 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Add Laplacian noise to alpha_hat_i, where 1 is the sensitivity
        alpha_hat[i] = laplace_mechanism(alpha[i],1,epsilon_prime)
        
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    return B

