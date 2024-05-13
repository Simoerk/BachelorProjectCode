import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism import binary_mechanism
from utils.load_dataset import load_dataset
import time

# Load the dataset
df_el = load_dataset("./Data/PrivIndustryConsumptionSumHour.csv", 1000000)


df_el=df_el.groupby('HourUTC')['ConsumptionkWh'].sum().reset_index()


# Select the 'consumptionkwh' column as a numpy array
sigma_el = df_el['ConsumptionkWh'].to_numpy()


# Algorithm 2: Binary mechanism
epsilon = 1  # Privacy parameter

#Revese sigma because new entreis are added at the end
sigma_el_flipped = np.flip(sigma_el)


# remov upper quantile and then use that to calculate the epsilon, then run on this dataset
upper_quantile = np.quantile(sigma_el_flipped, 0.99)
sigma_el_filtered = sigma_el_flipped[(sigma_el_flipped < upper_quantile)]


# scale sigma_el_flipped 
min_val_flip = 0
max_val_flip = np.max(sigma_el_flipped)
# Scale the array
sigma_el_flipped_scaled = (sigma_el_flipped - min_val_flip) / (max_val_flip - min_val_flip)


#Find max value in sigma_el_filtered and scaæe
min_val_fil = 0
max_val_fil = np.max(sigma_el_filtered)
sigma_el_filtered_scaled = (sigma_el_filtered - min_val_fil) / (max_val_fil - min_val_fil)



# Bin mech on data with high values 
T = len(sigma_el)
start_time = time.time()
B_t = binary_mechanism(T, epsilon, sigma_el_flipped_scaled)
end_time = time.time()

#print the time it took to run the mechanism loop
duration = end_time - start_time
print(f"The unfiltered data for the function took {duration} seconds to run.")

#scale up again
B_t = np.array(B_t)
B_t = B_t * (max_val_flip - min_val_flip) + min_val_flip

# Bin mech on data without high values
T_fil = len(sigma_el_filtered)
start_time = time.time()
B_t_fil = binary_mechanism(T_fil, epsilon, sigma_el_filtered_scaled)
end_time = time.time()

#print the time it took to run the mechanism loop
duration = end_time - start_time
print(f"The filtered data for the function took {duration} seconds to run.")

B_t_fil = np.array(B_t_fil)
B_t_fil = B_t_fil * (max_val_fil - min_val_fil) + min_val_fil


#Get the last value, meaning the final sum
last_value1 = B_t[-1]

last_value2 = B_t_fil[-1]


pd.DataFrame(B_t, columns=['CumSum']).to_csv("results/num_noisy_result.csv", index=False)
pd.DataFrame(B_t_fil, columns=['CumSum']).to_csv("results/num_fil_noisy_result.csv", index=False)
pd.DataFrame(np.cumsum(sigma_el_flipped), columns=['CumSum']).to_csv("results/num_result.csv", index=False)
pd.DataFrame(np.cumsum(sigma_el_filtered), columns=['CumSum']).to_csv("results/num_fil_result.csv", index=False)

print("done")
