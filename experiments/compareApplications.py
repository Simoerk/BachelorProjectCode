import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# UNDER CONSTRUCTION

# Make sure to run the following files:
# Generate_pure_dataset.py , Num2DUnbGeo.py , Num2DUnbGeoLoc.py
# They will generate the needed csv files
# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/real_consumption_sums.csv')
Num2DUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
Num2DUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
Num2DUnb_df =  pd.read_csv('results/NumMunUnb_noisy_result.csv')
Num2D_df = pd.read_csv('results/NumMun_noisy_result.csv')

#remove regions and DK in the last column of the geographical data
Num2DUnbGeoLoc_df = Num2DUnbGeoLoc_df.iloc[:, :-6]
Num2DUnbGeo_df = Num2DUnbGeo_df.iloc[:, :-6]


#Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(actual, Num2DUnbGeoLoc, Num2DUnbGeo, Num2DUnb, Num2D, muni):
    plt.figure()
    plt.plot(actual[muni], label='Actual')
    plt.plot(Num2DUnbGeoLoc[muni], label='Num2DUnbGeoLoc')
    plt.plot(Num2DUnbGeo[muni], label='Num2DUnbGeo')
    plt.plot(Num2DUnb[muni], label='Num2DUnb')
    plt.plot(Num2D[muni], label='Num2D')
    plt.legend()
    plt.title(f'Comparison of {muni} between Actual and Noisy Data')
    plt.show()


show_comparison_for_specific_muni(actual_df, Num2DUnbGeoLoc_df, Num2DUnbGeo_df, Num2DUnb_df, Num2D_df, '825')

show_comparison_for_specific_muni(actual_df, Num2DUnbGeoLoc_df, Num2DUnbGeo_df, Num2DUnb_df, Num2D_df, '101')