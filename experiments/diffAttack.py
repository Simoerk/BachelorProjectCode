import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from utils.scaleData import downScale
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc

# Experiment that attempts to attack the privacy of the NumMunUnbGeoLoc mechanism 
# in a simple manner 

# Calculate the likelihood of obtaining the noisy outputs
def laplace_likelihood(x, noisy_x, scale):
    return stats.laplace.pdf(noisy_x - x, scale=scale)

# Sensitivity of the query
sensitivity = 1.0

# Define the epsilon values
epsilon_values = [0.2, 0.5, 1, 5]

# Run the analysis for each epsilon value
results = {}

# Load the data
true_data = pd.read_csv('results/real_consumption_sums.csv', index_col=0)

# Downscale the data
true_data['101'], _ = downScale(true_data, '101')

# Extract the consumption values
true_consumptionof101 = true_data['101'].values

# Extract the last rows of the true dataframe
true_last_row = true_consumptionof101[-1]

# Extract the second last rows of the true dataframe
true_second_last_row = true_consumptionof101[-2]

for epsilon in epsilon_values:

    # Run the mechanism
    NumMunUnbGeoLoc(epsilon)

    # Load the noisy data
    noisy_data = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv', index_col=0)

    # Downscale the data
    noisy_data['101'], _ = downScale(noisy_data, '101')

    # Extract the consumption values
    noisy_consumptionof101 = noisy_data['101'].values

    # Extract the last rows of the noisy dataframe
    noisy_last_row = noisy_consumptionof101[-1]

    # Calculate the scale
    scale = sensitivity / epsilon
    p1 = laplace_likelihood(true_last_row, noisy_last_row, scale)
    p2 = laplace_likelihood(true_second_last_row, noisy_last_row, scale)
    result = (p1 / p2) <= np.exp(epsilon)
    results[epsilon] = (p1, p2, result)

# Print the results
for epsilon, (p1, p2, result) in results.items():
    print(f"Epsilon: {epsilon}")
    print(f"P1: {p1}")
    print(f"P2: {p2}")
    print(f"Result: {result}\n")
