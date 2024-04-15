import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
from utils.muniRegion import *

def load_dataset(): # Function that loads the dataset
    data = pd.read_csv("data/orderedMunicipality.csv")
    return data



# Differential privacy on Dataset with Municipality, time and housing/heating category
municipalities = load_dataset()

def geographical_Mechanism(t, epsilon, stream): 
    stream = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    alpha = [[], [], []]
    alpha_hat = [[], [], []]
    B_alpha = []
    B = []

    # Privacy parameter for the Laplacian mechanism MUST BE ALTERED AND PROVEN
    epsilon_prime = epsilon / (math.log(3))

    regionDictionary = give_regionDictionary()
    print("regionDictionary: ", regionDictionary)
    
    for region in regionDictionary:
        # Input municipalities in alpha and alpha_hat
        for muni in regionDictionary[region]:
            muni_consumption = stream[muni][t]
            alpha[0].append(muni_consumption)
            alpha_hat[0].append(muni_consumption + laplace_mechanism(1/epsilon_prime))
        
        # Input municipalities in B 
        B_alpha.append(alpha[0])
        B.append(alpha_hat[0])

        # Input region in alpha lists
        region_sum = sum(alpha[0])
        alpha[1].append(region_sum)
        alpha_hat[1].append(region_sum + laplace_mechanism(1/epsilon_prime))

        # Reset alpha lists
        alpha[0] = []
        alpha_hat[0] = []
    
    # Input regions in B
    B_alpha.append(alpha[1])
    B.append(alpha_hat[1])
    
    # Input the sum of regions for DK in B
    DK_sum = sum(alpha[1])
    B_alpha.append(DK_sum)
    B.append(DK_sum + laplace_mechanism(1/epsilon_prime))

    return B, B_alpha





def geographical_Binary_Mechanism(T, epsilon, stream):
    if T <= 0:
        raise ValueError("T must be a positive integer or float")
    stream = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    # Initialize alphas for time-tree
    length_alpha = int(math.log2(T)) + 1
    alpha = [[] for _ in range(length_alpha)]
    alpha_hat = [[] for _ in range(length_alpha)]

    B = [[] for _ in range(T)]

    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log(T))

    for t in range(1, T + 1):
        # Convert t to binary form
        bin_t = [int(x) for x in bin(t)[2:]]
        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t  # Pad with zeros to match alpha length

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        

        # Update alpha_i DU KOMMET HERTIL, LINE 92 SKAL GÅ ET ELEMENT I alpha_i_tree IGENNEM AD GANGEN OG LÆGGE DEM SAMMEN
        time_t = stream.iloc[t]["HourDK"]
        alpha_hat_i_tree, alpha_i_tree = geographical_Mechanism(time_t, epsilon, stream)
        alpha[i].append(sum(alpha[j] for j in range(i)) + stream[t-1])

        # Overwrite previous values with 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Add Laplacian noise to alpha_hat_i
        alpha_hat[i] = alpha[i] + laplace_mechanism(1/epsilon_prime)
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)

    return B