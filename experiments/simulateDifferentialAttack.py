import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc

# Load the datasets
true_data = pd.read_csv('results/real_consumption_sums.csv')
true_data101 = true_data['101']
true_data101_2 = true_data101[:-1]

differences = []

def simulateDifferentialAttack(epsilon):
    for _ in range(10):
        # Load the noisy data
        NumMunUnbGeoLoc(epsilon)
        noisy_data = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        mun101 = noisy_data['101']

        # Make a copy of the noisy data
        NumMunUnbGeoLoc(epsilon)
        noisy_data_copy = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        mun101_copy = noisy_data_copy['101']

        # Remove last element of mun101_copy
        mun101_copy = mun101_copy[:-1]

        difference = mun101.iloc[-1] - mun101_copy.iloc[-1]

        differences.append(difference)

    return differences

differences = simulateDifferentialAttack(1)

plt.hist(differences, bins=10)
plt.show()

print("Differences: ", differences)
print(f"Mean: {np.mean(differences)}")
