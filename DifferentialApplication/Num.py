import numpy as np
import pandas as pd
from Mechanisms.BinaryMechanism import binary_mechanism
from utils.load_dataset import load_dataset
import time

# Num(epsilon) applies the binary mechanism to the electricity dataset from Energinet
# Without municipalities
def Num(epsilon):

    # Load the dataset
    df_el = load_dataset("./Data/PrivIndustryConsumptionSumHour.csv", 1000000)

    # Group by HourUTC and sum the ConsumptionkWh to remove categories
    df_el = df_el.groupby('HourUTC')['ConsumptionkWh'].sum().reset_index()

    # Select the 'consumptionkwh' column as a numpy array
    sigma_el = df_el['ConsumptionkWh'].to_numpy()

    # Revese the 'stream' because the dataset is in reverse order
    sigma_el_flipped = np.flip(sigma_el)

    # Remove upper quantile to make the dataset more private
    upper_quantile = np.quantile(sigma_el_flipped, 0.99)
    sigma_el_filtered = sigma_el_flipped[(sigma_el_flipped < upper_quantile)]

    # We make two arrays
    # - One without high values in the dataset, good for privacy
    # - One with high values in the dataset, good for utlity

    # Scale the unfiltered array to be between 0 and 1
    min_val_flip = 0
    max_val_flip = np.max(sigma_el_flipped)
    sigma_el_flipped_scaled = (sigma_el_flipped - min_val_flip) / (max_val_flip - min_val_flip)

    # Scale the filtered array to be between 0 and 1 (Without high values)
    min_val_fil = 0
    max_val_fil = np.max(sigma_el_filtered)
    sigma_el_filtered_scaled = (sigma_el_filtered - min_val_fil) / (max_val_fil - min_val_fil)


    # Get the length of the array
    T = len(sigma_el)

    # Start a timer
    start_time = time.time()

    # Apply the binary mechanism to the unfiltered data
    B_t = binary_mechanism(T, epsilon, sigma_el_flipped_scaled)
    end_time = time.time()

    # Print the time it took to run the mechanism loop
    duration = end_time - start_time
    print(f"The unfiltered data for the function took {duration} seconds to run.")

    # Scale up again
    B_t = np.array(B_t)
    B_t = B_t * (max_val_flip - min_val_flip) + min_val_flip


    # Get the length of the filtered array
    T_fil = len(sigma_el_filtered)

    # Start a timer
    start_time = time.time()

    # Apply the binary mechanism to the filtered data
    B_t_fil = binary_mechanism(T_fil, epsilon, sigma_el_filtered_scaled)
    end_time = time.time()

    # Print the time it took to run the mechanism loop
    duration = end_time - start_time
    print(f"The filtered data for the function took {duration} seconds to run.")

    # Scale up again
    B_t_fil = np.array(B_t_fil)
    B_t_fil = B_t_fil * (max_val_fil - min_val_fil) + min_val_fil

    # Save the results
    pd.DataFrame(B_t, columns=['CumSum']).to_csv("results/num_noisy_result.csv", index=False)
    pd.DataFrame(B_t_fil, columns=['CumSum']).to_csv("results/num_fil_noisy_result.csv", index=False)
    pd.DataFrame(np.cumsum(sigma_el_flipped), columns=['CumSum']).to_csv("results/num_result.csv", index=False)
    pd.DataFrame(np.cumsum(sigma_el_filtered), columns=['CumSum']).to_csv("results/num_fil_result.csv", index=False)

    print("done")

# Main function that runs when the file is executed
if __name__ == "__main__":
    Num(1)