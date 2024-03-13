import numpy as np
import pandas as pd
import math

scales = 0

# Load the dataset
print("Loading the diabetes dataset...")
df_dia = pd.read_csv("./Data/diabetes_binary_health_indicators_BRFSS2015.csv")
print("Dataset loaded successfully!")

# Select the 'Diabetes_binary' column as a numpy array
print("Selecting the 'Diabetes_binary' column...")
sigma_dia = df_dia['Diabetes_binary'].to_numpy()
print("Column selected successfully!")

# Load the dataset
print("Loading the el dataset...")
df_el = pd.read_csv("./Data/PrivIndustryConsumptionSumHour.csv")
print("Dataset loaded successfully!")


df_el=df_el.groupby('HourUTC')['ConsumptionkWh'].sum().reset_index()
print("df_el:", df_el)

# Select the 'Diabetes_binary' column as a numpy array
print("Selecting the 'ConsumptionkWh' column...")
sigma_el = df_el['ConsumptionkWh'].to_numpy()
print("Column selected successfully!")




# Function to apply the Laplace mechanism for differential privacy
def laplace_mechanism(epsilon):
    # The sensitivity of a sum query is 1
    sensitivity = 1
    scale = sensitivity / epsilon
    # Generate Laplace noise
    noise = np.random.laplace(0, scale)
    return noise


def two_level_mechanism(T, epsilon, sigma, B):
    # Initialize alpha and beta
    alpha = np.zeros(T)
    beta = np.zeros(T // B + (T % B > 0))  
    
    # Mechanism
    for t in range(1, T + 1):
        lap = laplace_mechanism(epsilon)
        alpha[t-1] = sigma[t-1] + lap
        print("sigma: " , sigma[t-1])
        print("alpha: ", alpha[t-1])
        print("lap: " , lap)
        q, r = divmod(t, B)
        if r == 0:  # Check if t is at the end of a bucket
            print("t: \n" , t)
            lap = laplace_mechanism(epsilon)
            beta[q-1] = sum(sigma[t-B+1:t]) + lap
            print("sum: " , sum(sigma[t-B+1:t]))
            print("lap: " , lap)
            print("beta: " , beta[q-1])
        
        # Calculate D(t)
        D_t = sum(beta[:q]) + sum(alpha[q*B+1:t])
        yield D_t





def binary_mechanism(T, epsilon, stream):
    # Initialize alphas
    alpha = [0] * (int(math.log2(T)) + 1)
    alpha_hat = [0] * (int(math.log2(T)) + 1)
    
    # Privacy parameter for the Laplacian mechanism
    epsilon_prime = epsilon / (math.log(T))
    
    # Output estimate at each time step
    B = [0] * T
    
    for t in range(1, T + 1):
        # Convert t to binary form
        bin_t = [int(x) for x in bin(t)[2:]]

        bin_t = [0] * (len(alpha) - len(bin_t)) + bin_t  # Pad with zeros to match alpha length

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

        # Update alpha_i
        alpha[i] = sum(alpha[j] for j in range(i)) + stream[t-1]

        # Overwrite previous values with 0
        for j in range(i):
            alpha[j] = 0.0
            alpha_hat[j] = 0.0
        
        # Add Laplacian noise to alpha_hat_i
        alpha_hat[i] = alpha[i] + laplace_mechanism(1/epsilon_prime)
        
        # Calculate the noisy p-sum for output
        B[t-1] = sum(alpha_hat[j] for j, bit in enumerate(bin_t) if bit == 1)
    return B



#T for Diabetes
T = len(sigma_dia)  # Number of records in the 'diabetes_binary' column
#T = 1000
epsilon = 0.9  # Differential privacy parameter

# B value used for two level mechanism, B is Block size 
B = int(math.ceil(math.sqrt(T)))
#print("B: ", B)




"""
# Algortohm 1: Two level counting mechanism
print("Applying the two-level mechanism...")
estimates = list(two_level_mechanism(T, epsilon, sigma_dia, B))
print("Mechanism applied successfully!")

# Print or save the results as needed
print(estimates) 
print("real: ", sigma_dia.sum())
print("len: ", len(sigma_dia))
"""




#sum the consumption row to get the real sum value
print("real: ", sigma_el.sum())



# Algorithm 2: Binary mechanism
epsilon = 10  # Privacy parameter

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
min_val = np.min(sigma_el_flipped)
max_val = np.max(sigma_el_flipped)
# Scale the array
sigma_el_flipped_scaled = (sigma_el_flipped - min_val) / (max_val - min_val)


#scale sigma_el_filtered
# Calculate min and max of the array
min_val = np.min(sigma_el_filtered)
max_val = np.max(sigma_el_filtered)
# Scale the array
sigma_el_filtered_scaled = (sigma_el_filtered - min_val) / (max_val - min_val)
print("max: ", max_val)



# Bin mech on data with high values 
T = len(sigma_el)
print("T: ", T)
B_t = binary_mechanism(T, epsilon, sigma_el_flipped_scaled)
#print(B_t)

# Bin mech on data without high values
T_fil = len(sigma_el_filtered)
print("T_fil: ", T_fil)
B_t_fil = binary_mechanism(T_fil, epsilon, sigma_el_filtered_scaled)
#print(B_t_fil)



#Get the last value, meaning the final sum
last_value1 = B_t[-1]
print("las1: ", last_value1)

last_value2 = B_t_fil[-1]
print("las2: ", last_value2)



# Be able to query certain intervals

with open("Data/B_t.txt", "w") as f:
    for item in B_t:
        # Write each item on a new line
        f.write("%s\n" % item)

with open("Data/B_t_filtered.txt", "w") as f:
    for item in B_t_fil:
        # Write each item on a new line
        f.write("%s\n" % item)



