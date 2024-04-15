import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
from utils.muniRegion import *

<<<<<<< Updated upstream
def extractConsumption(hourDK): 
    
    return
    
def geographical_Mechanism_DK(epsilon, stream):
    alpha
    return
=======
def load_dataset(): # Function that loads the dataset
    data = pd.read_csv("data/orderedMunicipality.csv")
    return data

# Differential privacy on Dataset with Municipality, time and housing/heating category
municipalities = load_dataset()

def geographical_Mechanism(t, epsilon, stream): 
    stream = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    alpha = [[], [], []]
    alpha_hat = [[], [], []]
    B_alpha = [[], [], []]
    B = [[], [], []]

    # Privacy parameter for the Laplacian mechanism MUST BE ALTERED AND PROVEN
    epsilon_prime = epsilon / (math.log(3))

    # Initialization of geographical lists, muni, region and Denmark
    regions = ["Hovedstaden", "Sjaelland", "Syddanmark", "Midtjylland", "NordJylland"]
    muni_iterators = [29, 17, 22, 19, 11]
    regionDictionary = give_regionDictionary()
    print("regionDictionary: ", regionDictionary)
    
    for region in regions:
        # Input municipalities in alpha and alpha_hat
        for muni in regionDictionary[region]:
            muni_consumption = stream[muni][t]
            alpha[0].append(muni_consumption)
            alpha_hat[0].append(muni_consumption + laplace_mechanism(1/epsilon_prime))
        B_alpha = alpha[0]
        B[0] = alpha_hat[0]

        # Input region in alpha lists
        region_sum = sum(alpha[0])
        alpha[1].append(region_sum)
        alpha_hat[1].append(region_sum + laplace_mechanism(1/epsilon_prime))

        # Reset alpha lists
        alpha[0] = []
        alpha_hat[0] = []

    return B, B_alpha




>>>>>>> Stashed changes

def geographical_Binary_Mechanism(T, epsilon, stream):
    if T <= 0:
        raise ValueError("T must be a positive integer or float")
    stream = stream.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    # Initialize alphas for time-tree
    length_alpha = int(math.log2(T)) + 1
    alpha = [[0] * length_alpha for _ in range(length_alpha)]
    alpha_hat = [[0] * length_alpha for _ in range(length_alpha)]

    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log(T))
    
    # Output estimate at each time step for each geographical tree
    B = [[] for _ in range(T)]
    B_G = [0] * 104
    # Output lists of the geographical tree 
    B_G_alpha = []
    B_G_hat = []

    G_alpha = [[] for _ in range(104)]  # Initialize G_alpha with T empty lists
    G_alpha_hat = [[] for _ in range(104)]  # Initialize G_alpha with T empty lists

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
        for muni_number in municipalities["number"]:
            muni_number = int(muni_number)
            # Initialize alphas for geographical-tree
            G_alpha[muni_number].append(stream[muni_number][t])
            G_alpha_hat[muni_number].append((stream[muni_number][t])+laplace_mechanism(1/epsilon_prime))
            region = give_region().get(muni_number, None)
            G_alpha[t][1].append(region, (stream(t,muni_number)))
<<<<<<< Updated upstream
=======
            B_G[muni_number] = G_alpha_hat[muni_number][t]

        
        region_sums = {}
>>>>>>> Stashed changes

        for region, consumption in G_alpha[t][1]:
            if region in G_alpha[t][1]:
                G_alpha[t][1][region] += consumption
            else:
                G_alpha[t][1][region] = consumption

        
        
        print(region_sums)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Overwrite previous values with 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    print(alpha)
    print(alpha_hat)
    print(G_alpha)
    print(G_alpha_hat)
    return B