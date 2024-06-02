import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc

# This file is used to compare the results of the local and global applications with plots  

# Run the applications to generate the noisy result files
NumMunUnbGeo(1)
NumMunUnbGeoLoc(1)

# Run utils.generatePureDataTree.py to generate regional_consumption_sums.csv

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
local_noisy_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
global_noisy_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')

#Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(actual, local_noisy, global_noisy, muni):
    plt.figure()
    plt.plot(actual[muni], label='Actual')
    plt.plot(local_noisy[muni], label='Local Noisy')
    plt.plot(global_noisy[muni], label='Global Noisy')
    plt.legend()
    plt.title(f'Comparison of {muni} between Actual and Noisy Data')
    plt.show()


show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, '825')

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, '101')

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, 'DK')

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, 'Hovedstaden')

show_comparison_for_specific_muni(actual_df, local_noisy_df, global_noisy_df, 'Nordjylland')