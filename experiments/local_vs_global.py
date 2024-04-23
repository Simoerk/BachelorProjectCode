import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# UNDER CONSTRUCTION

# Make sure to run the following files:
# Generate_pure_dataset.py , Num2DUnbGeo.py , Num2DUnbGeoLoc.py
# They will generate the needed csv files
# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
local_noisy_df = pd.read_csv('results/Num2DUnbGeoLoc_noisy_result.csv')
global_noisy_df = pd.read_csv('results/Num2DUnbGeo_noisy_result.csv')

#Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(actual, local_noisy, global_noisy, muni):
    plt.figure()
    plt.plot(actual[muni], label='Actual')
    plt.plot(local_noisy[muni], label='Local Noisy')
    plt.plot(global_noisy[muni], label='Global Noisy')
    plt.legend()
    plt.title(f'Comparison of {muni} between Actual and Noisy Data')
    plt.show()

def calculate_std_deviation(actual, local_noisy, global_noisy):
    actual = actual.iloc[1:, 1:]
    local_noisy = local_noisy.iloc[1:, 1:]
    global_noisy = global_noisy.iloc[1:, 1:]

    # Calculate deviations for local_noisy_df
    deviation_local = local_noisy - actual

    # Calculate deviations for global_noisy_df
    deviation_global = global_noisy - actual

    # Calculate standard deviation for local_noisy_df
    std_dev_local = deviation_local.std()

    # Calculate standard deviation for global_noisy_df
    std_dev_global = deviation_global.std()

    print("Standard Deviation for Local Noisy Dataframe:")
    print(std_dev_local)
    print("\nStandard Deviation for Global Noisy Dataframe:")
    print(std_dev_global)

    return std_dev_local, std_dev_global


std_dev_local, std_dev_global = calculate_std_deviation(actual_df, local_noisy_df, global_noisy_df)

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, '825')

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, '101')