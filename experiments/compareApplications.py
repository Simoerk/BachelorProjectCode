import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from DifferentialApplication.NumMun import NumMun
from DifferentialApplication.NumMunUnb import NumMunUnb
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc

# This file is used to compare the results of the different applications with plots

# Make sure to run the files:
# They will generate the needed csv files

NumMun(1)
NumMunUnb(1)
NumMunUnbGeo(1)
NumMunUnbGeoLoc(1)

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/real_consumption_sums.csv')
NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
NumMunUnb_df =  pd.read_csv('results/NumMunUnb_noisy_result.csv')
NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')

# Remove regions and DK in the last column of the geographical data
NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, :-6]
NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]

# Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(df_list, label_list, muni):
    plt.figure()
    for (df, lab) in zip(df_list, label_list):
        plt.plot(df[muni], label=lab)
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframes: {label_list}')
    plt.xlabel('Number of hours in the given period')
    plt.ylabel('Consumption in kWh')
    plt.show()

# Show the comparison for a specific municipality
show_comparison_for_specific_muni([actual_df, NumMunUnbGeoLoc_df, NumMunUnbGeo_df, NumMunUnb_df, NumMun_df], ['Actual', 'NumMunUnbGeoLoc', 'NumMunUnbGeo', 'NumMunUnb', 'NumMun'], '825')
show_comparison_for_specific_muni([actual_df, NumMunUnbGeoLoc_df, NumMunUnbGeo_df, NumMunUnb_df, NumMun_df], ['Actual', 'NumMunUnbGeoLoc', 'NumMunUnbGeo', 'NumMunUnb', 'NumMun'], '101')