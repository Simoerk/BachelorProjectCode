import pandas as pd
import numpy as np
import math
from utils.laplace import laplace_mechanism

# Modify the binary mechanism function to handle municipality consumption data
def binary_mechanism_municipalities(T, epsilon, stream):
    consumption_data = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    epsilon_prime = epsilon / (math.log(T))
    B = [0] * T
    
    for t in range(1, T + 1):
        bin_t = [int(x) for x in bin(t)[2:]]
        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t
        
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        print(consumption_data)
        for municipality in range(len(consumption_data.columns)):
            alpha[i] += consumption_data.iloc[t-1, municipality]
            alpha_hat[i] = alpha[i] + laplace_mechanism(1/epsilon_prime)

        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        B[t-1] = alpha_hat[i]
        
    return B

# Example usage:
# T = number of time steps
# epsilon = privacy parameter
# consumption_data = DataFrame containing consumption data for each municipality
# B = binary_mechanism_municipalities(T, epsilon, consumption_data)
