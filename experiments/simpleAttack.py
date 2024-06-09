import pandas as pd
import numpy as np
from scipy.optimize import minimize
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
import math
import utils.generatePureDataTree as gPDT



epsilons = [0.1, 0.5, 1, 5, 10, 20]

for epsilon in epsilons:

    NumMunUnbGeo(epsilon)

    # Run the main function from utils.generatePureDataTree 
    # with results/NumMunUnbGeo_downscaled_noisy_result.csv as input
    # and results/NumMunUnbGeo_downscaled_region_result.csv as output
    # results/NumMunUnbGeo_downscaled_noisy_result.csv is generated using the NumMunUnbGeo application
    # by uncommenting the line where the downscaled data is saved to a CSV file
    #gPDT.main()
    

    df_noisy = pd.read_csv('results/NumMunUnbGeo_downscaled_noisy_result.csv')
    df_real = pd.read_csv('results/NumMunUnbGeo_downscaled_region_result.csv')

    df_real = df_real.cumsum()

    # Define columns to work on
    columns_to_use = ['101', 'Hovedstaden', 'DK']

    # Function to get log2 rows
    def get_log2_indices(df):
        return [2**i - 1 for i in range(int(np.log2(len(df))) + 1) if 2**i - 1 < len(df)]

    def get_log2_rows(df, columns):
        log2_indices = get_log2_indices(df)
        return df.iloc[log2_indices][columns], log2_indices

    # Extract log2 rows and their original indices
    log2_noisy, log2_noisy_indices = get_log2_rows(df_noisy, columns_to_use)
    log2_real, log2_real_indices = get_log2_rows(df_real, columns_to_use)


    # Subtract first value from all log2 rows in real data
    first_real_value = log2_real['101'].iloc[0]
    adjusted_log2_real = log2_real.copy()
    adjusted_log2_real.loc[1:] = log2_real.loc[1:] - first_real_value
    adjusted_log2_real.loc[:1,'Hovedstaden'] = log2_real.loc[:1,'Hovedstaden'] - first_real_value
    adjusted_log2_real.loc[:1,'DK'] = log2_real.loc[:1,'DK'] - first_real_value

    # Prepare list for MLE with original indices
    data_for_mle = []
    original_indices = []

    # Add first log2 row from noisy data
    data_for_mle.extend(log2_noisy.iloc[0].values)
    original_indices.extend([log2_noisy_indices[0]] * len(log2_noisy.columns))

    # Add subsequent rows after adjustment
    for idx in range(1, len(log2_noisy)):
        diff = log2_noisy.iloc[idx].values - adjusted_log2_real.iloc[idx].values
        data_for_mle.extend(diff)
        original_indices.extend([log2_noisy_indices[idx]] * len(log2_noisy.columns))

    # Convert to numpy array
    data_for_mle = np.array(data_for_mle)

    # Define the noise parameters
    theta = 0.5
    a_i = lambda i: (i + 1)**(1 + theta)
    scale_param = lambda i: (a_i(i) * 3) / epsilon

    # Function to find i from index
    def find_i(t):
        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
            
            # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]

            # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse() # bin_t was in reverse order
        return next(i for i, bit in enumerate(bin_t) if bit != 0)

    # Define the likelihood function
    def likelihood(X, data, epsilon, theta, indices):
        likelihood = 0
        for k, elm in enumerate(data):
            i = find_i(indices[k]+1)
            #print("i: ", i)
            b = scale_param(i)
            likelihood += np.log((1 / (2 * b)) * np.exp(- np.abs(elm - X) / b))
        return -likelihood  # Negative because we minimize

    # Initial guess for X (mean of data_for_mle)
    initial_X = np.mean(data_for_mle)
    initial_X = np.clip(initial_X, 0, 1)
    

    # Perform optimization
    result = minimize(likelihood, initial_X, args=(data_for_mle, epsilon, theta, original_indices), method='L-BFGS-B', bounds=[(0, 1)])

    if result.success:
        estimated_X = result.x
        real_value = df_real.loc[0, '101']
        print("\nepsilon: ", epsilon)
        print("inital_X: ", initial_X)
        print(f"Estimated X: {estimated_X}")
        print(f"Real X: {real_value}")   
    else:
        raise ValueError("Optimization failed")
