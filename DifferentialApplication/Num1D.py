import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism import binary_mechanism

# Load the dataset
print("Loading the el dataset...")
df_el = pd.read_csv("./Data/PrivIndustryConsumptionSumHour.csv")
print("Dataset loaded successfully!")


df_el=df_el.groupby('HourUTC')['ConsumptionkWh'].sum().reset_index()
print("df_el:", df_el)

# Select the 'consumptionkwh' column as a numpy array
print("Selecting the 'ConsumptionkWh' column...")
sigma_el = df_el['ConsumptionkWh'].to_numpy()
print("Column selected successfully!")


#sum the consumption row to get the real sum value
print("real: ", sigma_el.sum())


# Algorithm 2: Binary mechanism
epsilon = 0.1  # Privacy parameter

#Revese sigma because new entreis are added at the end
sigma_el_flipped = np.flip(sigma_el)



# remove lower and upper quantile and then use that to calculate the epsilon, then run on this dataset
lower_quantile = np.quantile(sigma_el_flipped, 0.25)
upper_quantile = np.quantile(sigma_el_flipped, 0.99)

#This part doesnt matter anymore
#IQR = upper_quantile - lower_quantile
#upper_bound = upper_quantile + 1.5 * IQR
#print("upper: ", upper_bound)
# Filter the array to only include values between the lower and upper quantile
#sigma_el_Upper = sigma_el_flipped[(sigma_el_flipped > upper_bound)]
#print("sigma_el_remUpper: ", len(sigma_el_Upper))

sigma_el_filtered = sigma_el_flipped[(sigma_el_flipped < upper_quantile)]


#scale sigma_el_flipped 
# Calculate min and max of the array
min_val_flip = 0
max_val_flip = np.max(sigma_el_flipped)
# Scale the array
sigma_el_flipped_scaled = (sigma_el_flipped - min_val_flip) / (max_val_flip - min_val_flip)


#scale sigma_el_filtered
# Calculate min and max of the array
min_val_fil = 0
max_val_fil = np.max(sigma_el_filtered)
# Scale the array
sigma_el_filtered_scaled = (sigma_el_filtered - min_val_fil) / (max_val_fil - min_val_fil)
#print("max: ", max_val_fil)



# Bin mech on data with high values 
T = len(sigma_el)
print("T: ", T)
B_t = binary_mechanism(T, epsilon, sigma_el_flipped_scaled)

#scale up again
B_t = np.array(B_t)
B_t = B_t * (max_val_flip - min_val_flip) + min_val_flip

#print(B_t)

# Bin mech on data without high values
T_fil = len(sigma_el_filtered)
print("T_fil: ", T_fil)
B_t_fil = binary_mechanism(T_fil, epsilon, sigma_el_filtered_scaled)

B_t_fil = np.array(B_t_fil)
B_t_fil = B_t_fil * (max_val_fil - min_val_fil) + min_val_fil

#print(B_t_fil)


#Get the last value, meaning the final sum
last_value1 = B_t[-1]
print("las1: ", last_value1)

last_value2 = B_t_fil[-1]
print("las2: ", last_value2)



# Be able to query certain intervals

# with open("results/B_t.txt", "w") as f:
#     for item in B_t:
#         # Write each item on a new line
#         f.write("%s\n" % item)

# with open("results/B_t_filtered.txt", "w") as f:
#     for item in B_t_fil:
#         # Write each item on a new line
#         f.write("%s\n" % item)


pd.DataFrame(B_t, columns=['NoisyCumSum']).to_csv("results/num1D_noisy_result.csv", index=False)
pd.DataFrame(B_t_fil, columns=['FilteredNoisyCumSum']).to_csv("results/num1D_fil_noisy_result.csv", index=False)
pd.DataFrame(np.cumsum(sigma_el_flipped), columns=['CumSum']).to_csv("results/num1D_result.csv", index=False)
pd.DataFrame(np.cumsum(sigma_el_filtered), columns=['CumSum']).to_csv("results/num1D_fil_result.csv", index=False)

print("done")
