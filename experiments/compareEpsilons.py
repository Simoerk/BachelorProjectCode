import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnb import NumMunUnb
from DifferentialApplication.NumMun import NumMun
from experiments.compareApplications import show_comparison_for_specific_muni


# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/real_consumption_sums.csv')
#NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
#NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
#NumMunUnb_df =  pd.read_csv('results/NumMunUnb_noisy_result.csv')
#NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')

#remove regions and DK in the last column of the geographical data
#NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, :-6]
#NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]


def compare_epsilons_across_applications():
    epsilons = [0.1, 0.3, 0.5, 1, 1.5, 5]

    for epsilon in epsilons:
        print("running epsilon: ", epsilon)
        print("\nrunning NumMunUnbGeoLoc")
        NumMunUnbGeoLoc(epsilon)
        print("\nrunning NumMunUnbGeo")
        NumMunUnbGeo(epsilon)
        NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
        show_comparison_for_specific_muni([actual_df, NumMunUnbGeoLoc_df, NumMunUnbGeo_df], ['Actual','NumMunUnbGeoLoc', 'NumMunUnbGeo', 'with epsilon: ', epsilon], muni)

# def find_closest_muni_to_avg():
#     #Find the average of the last row of the actual data
#     count = 0
#     for column in actual_df.columns:
#         count += actual_df[column].iloc[-1]
#     avg = count/len(actual_df.columns)
#     #Find the consumption of the last row closest to the average
#     abs_diff = 0
#     for column in actual_df.columns:
#         if abs(actual_df[column].iloc[-1] - avg) < abs_diff:
#             abs_diff = abs(actual_df[column].iloc[-1] - avg)
#             closest_muni = column
#     print(f"The municipality closest to the average consumption is: {closest_muni}")
#     return closest_muni

def find_closest_muni_to_avg():
    #Remove first column of actual_df
    actual_df_new = actual_df.iloc[:, 1:]

    # Calculate the average of the last row of the actual data
    last_row = actual_df_new.iloc[-1]
    avg = last_row.mean()
    
    # Find the column (municipality) with the consumption closest to the average
    closest_muni = (last_row - avg).abs().idxmin()
    
    print(f"The municipality closest to the average consumption is: {closest_muni}")
    return closest_muni


def compare_applications_across_epsilons(muni):
    epsilons = [0.1, 0.3, 0.5, 1, 1.5, 5]
    
    plt.figure()
    for epsilon in epsilons:
        NumMun(epsilon)
        df = pd.read_csv('results/NumMun_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMun with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMun and the actual data')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnb(epsilon)
        df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnb with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnb and the actual data')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnbGeo(epsilon)
        df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnbGeo with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnbGeo and the actual data')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnbGeoLoc(epsilon)
        df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnbGeoLoc with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnbGeoLoc and the actual data')
    plt.show()


compare_applications_across_epsilons('101')
