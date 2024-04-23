import numpy as np
import pandas as pd
import math
from Mechanisms.TwoLevelMechanism import two_level_mechanism


# Load the dataset
print("Loading the diabetes dataset...")
df_dia = pd.read_csv("./Data/diabetes_binary_health_indicators_BRFSS2015.csv")
print("Dataset loaded successfully!")

# Select the 'Diabetes_binary' column as a numpy array
print("Selecting the 'Diabetes_binary' column...")
sigma_dia = df_dia['Diabetes_binary'].to_numpy()
print("Column selected successfully!")



#T for Diabetes
T = len(sigma_dia)  # Number of records in the 'diabetes_binary' column
#T = 1000
epsilon = 0.1  # Differential privacy parameter

# B value used for two level mechanism, B is Block size 
B = int(math.ceil(math.sqrt(T)))
#print("B: ", B)




# Algortohm 1: Two level counting mechanism
print("Applying the two-level mechanism...")
estimates = list(two_level_mechanism(T, epsilon, sigma_dia, B))
print("Mechanism applied successfully!")

# Print or save the results as needed
#print(estimates) 
#print("real: ", sigma_dia.sum())
#print("len: ", len(sigma_dia))


pd.DataFrame(estimates).to_csv("results/Bin1D_noisy_result.csv", index=False)
cumulative_sums = np.cumsum(sigma_dia)
pd.DataFrame(cumulative_sums, columns=['Actual Sum']).to_csv("results/Bin1D_result.csv", index=False)
