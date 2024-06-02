import numpy as np
import pandas as pd
import math
from Mechanisms.TwoLevelMechanism import two_level_mechanism
from utils.load_dataset import load_dataset
import time
from utils.muniRegion import *

# Bin(epsilon) applies the two-level mechanism to the diabetes dataset
def Bin(epsilon):

    # Load the dataset
    df_dia = load_dataset("./Data/diabetes_binary_health_indicators_BRFSS2015.csv", 1000000)

    # Select the 'Diabetes_binary' column as a numpy array
    sigma_dia = df_dia['Diabetes_binary'].to_numpy()

    # Number of elements in the dataset
    T = len(sigma_dia)  

    # B value used for two level mechanism, B is Block size 
    B = int(math.ceil(math.sqrt(T)))

    # Algorithm 1: Two level counting mechanism
    print("Applying the two-level mechanism...")

    # Used for timing the mechanism loop
    start_time = time.time()

    # Apply the two-level mechanism and make a list of noisy data
    estimates = list(two_level_mechanism(T, epsilon, sigma_dia, B))
    end_time = time.time()

    #print the time it took to run the mechanism loop
    duration = end_time - start_time
    print(f"The function took {duration} seconds to run.")

    print("Mechanism applied successfully!")


    #Save results
    pd.DataFrame({'Sum': estimates}).to_csv("results/Bin_noisy_result.csv", index=False)
    cumulative_sums = np.cumsum(sigma_dia)
    pd.DataFrame(cumulative_sums, columns=['Sum']).to_csv("results/Bin_result.csv", index=False)

# Main loop to run the Bin function when running this file
if __name__ == "__main__":
    Bin(1)