import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
from utils.muniRegion import *

def extractConsumption(hourDK): 
    
    return
    
def geographical_Mechanism_DK(epsilon, stream):
    alpha
    return

def geographical_Binary_Mechanism(T, epsilon, stream):
    stream = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    # Initialize alphas for time-tree
    alpha = [[] for _ in range(int(math.log2(T)) + 1)]
    alpha_hat = [[] for _ in range(int(math.log2(T)) + 1)]

    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log(T))
    
    # Output estimate at each time step for each geographical tree
    B = [[]] * T
    
    # Output lists of the geographical tree 
    B_G_alpha = []
    B_G_hat = []

    G_alpha = [[],[],[]]
    G_alpha_hat = [[],[],[]]

    for t in range(1, T + 1):
        # Convert t to binary form
        bin_t = [int(x) for x in bin(t)[2:]]
        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t  # Pad with zeros to match alpha length

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        G_i = 0 
        
        iterator = 0
        iterator_list = count_regions()
        # Geographical loop to iterate over municipalities
        for muni_number in give_region():
            muni_number = int(muni_number)
            # Initialize alphas for geographical-tree
            G_alpha[t][0].append(stream(t,muni_number))
            G_alpha_hat[t][0].append(stream(t,muni_number)+laplace_mechanism(1/epsilon_prime))
            region = give_region().get(muni_number, None)
            G_alpha[t][1].append(region, (stream(t,muni_number)))

        for region, consumption in G_alpha[t][1]:
            if region in G_alpha[t][1]:
                G_alpha[t][1][region] += consumption
            else:
                G_alpha[t][1][region] = consumption

        
        
        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Overwrite previous values with 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    return B

