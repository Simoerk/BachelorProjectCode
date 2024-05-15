import pandas as pd
import numpy as np
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from experiments.compareApplications import show_comparison_for_specific_muni


# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/real_consumption_sums.csv')
NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
NumMunUnb_df =  pd.read_csv('results/NumMunUnb_noisy_result.csv')
NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')

#remove regions and DK in the last column of the geographical data
#NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, :-6]
#NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]


def compare_epsilons_across_applications():
    epsilons = [5]

    for epsilon in epsilons:
        print("running epsilon: ", epsilon)
        print("\nrunning NumMunUnbGeoLoc")
        NumMunUnbGeoLoc(epsilon)
        print("\nrunning NumMunUnbGeo")
        NumMunUnbGeo(epsilon)
        NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
        show_comparison_for_specific_muni([actual_df, NumMunUnbGeoLoc_df, NumMunUnbGeo_df], ['Actual','NumMunUnbGeoLoc', 'NumMunUnbGeo', 'with epsilon: ', epsilon], '825')


def compare_applications_across_epsilons():
    df_list