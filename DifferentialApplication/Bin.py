import numpy as np
import pandas as pd
import math
from Mechanisms.TwoLevelMechanism import two_level_mechanism
from utils.load_dataset import load_dataset
import time
from utils.muniRegion import *

# Load the dataset
df_dia = load_dataset("./Data/diabetes_binary_health_indicators_BRFSS2015.csv", 1000000)


# Select the 'Diabetes_binary' column as a numpy array
sigma_dia = df_dia['Diabetes_binary'].to_numpy()




#T for Diabetes
T = len(sigma_dia)  # Number of records in the 'diabetes_binary' column
epsilon = 0.1  # Differential privacy parameter

# B value used for two level mechanism, B is Block size 
B = int(math.ceil(math.sqrt(T)))



# Algortohm 1: Two level counting mechanism
print("Applying the two-level mechanism...")
start_time = time.time()
estimates = list(two_level_mechanism(T, epsilon, sigma_dia, B))
end_time = time.time()

#print the time it took to run the mechanism loop
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")

print("Mechanism applied successfully!")


#Save results
pd.DataFrame(estimates).to_csv("results/Bin1D_noisy_result.csv", index=False)
cumulative_sums = np.cumsum(sigma_dia)
pd.DataFrame(cumulative_sums, columns=['Actual Sum']).to_csv("results/Bin1D_result.csv", index=False)


