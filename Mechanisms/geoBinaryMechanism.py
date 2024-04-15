import pandas as pd
import numpy as np
import math
from utils.laplace import laplace_mechanism

# Modify the binary mechanism function to handle municipality consumption data
# def binary_mechanism_municipalities(T, epsilon, stream):
#     consumption_data = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

#     alpha = [0] * (int(math.log2(T)) + 1)
#     alpha_hat = [0] * (int(math.log2(T)) + 1)
#     epsilon_prime = epsilon / (math.log(T))
#     B = [0] * T
    
#     for t in range(1, T + 1):
#         bin_t = [int(x) for x in bin(t)[2:]]
#         bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t
        
#         bin_t.reverse()
#         i = next(i for i, bit in enumerate(bin_t) if bit != 0)

#         for municipality in range(len(consumption_data.columns)):
#             alpha[i] += consumption_data.loc[t, municipality]
#             for j in range(i):
#                 alpha[j] = 0.0
#                 alpha_hat[j] = 0.0
#             alpha_hat[i] = sum(alpha[j] for j, bit in enumerate(bin_t) if bit == 1) + laplace_mechanism(1/epsilon_prime)
        
#         B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
        
#     return B


#WORKING SOMEWHAT
# def binary_mechanism_municipalities(T, epsilon, stream):
#     consumption_data = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
#     alpha = [0] * (int(math.log2(T)) + 1)
#     epsilon_prime = epsilon / (math.log(T))
    
#     result = pd.DataFrame(index=range(1, T + 1), columns=consumption_data.columns)
    
#     unique_times = consumption_data.index

#     for t in range(1, T + 1):
#         bin_t = [int(x) for x in bin(t)[2:]]
#         bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t
        
#         bin_t.reverse()
#         i = next(i for i, bit in enumerate(bin_t) if bit != 0)

#         for municipality in consumption_data.columns:
#             alpha[i] += consumption_data.loc[unique_times[t-1], municipality]
#             for j in range(i):
#                 alpha[j] = 0.0
#             alpha_hat = sum(alpha[j] for j, bit in enumerate(bin_t) if bit == 1) + laplace_mechanism(1/epsilon_prime)
#             result.loc[t, municipality] = alpha_hat
        
#     return result

def binary_mechanism_municipalities(T, epsilon, stream):
    consumption_data = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    epsilon_prime = epsilon / (math.log(T))
    
    result = pd.DataFrame(index=range(1, T + 1), columns=consumption_data.columns)
    
    unique_times = consumption_data.index

    for t in range(1, T + 1):
        bin_t = [int(x) for x in bin(t)[2:]]
        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t
        
        bin_t.reverse()
        # Handle the case where bin_t is all zeros
        if all(bit == 0 for bit in bin_t):
            i = len(bin_t)  # Set i to the end of the list
        else:
            i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        alpha[i] += consumption_data.loc[unique_times[t-1]]
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        print(i)
        alpha_hat[i] = np.dot(alpha[i], bin_t) + laplace_mechanism(1/epsilon_prime)
        result.loc[t] = alpha_hat
        
    return result
