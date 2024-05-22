import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.scale import downScaleDf, upScaleDf, upScale, downScale
import math
from utils.clipData import clip_pr_column
from DifferentialApplication.NumMun import NumMun
from DifferentialApplication.Num import Num
from DifferentialApplication.Bin import Bin
from scipy.stats import gaussian_kde
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnb import NumMunUnb

def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df

# Function to calculate differences within each column
def calculate_differences(df):
    diff_df = df.apply(lambda x: x.diff().fillna(x.iloc[0]))
    return diff_df


# should be saved to differences_df.to_csv(f"results/Synthetic/{name}_syn_epsilon={epsilon}.csv", index=False)

# epsilons to test
epsilons = [2, 1, 0.5]
#epsilons = [1]

epsilon_errors = {epsilon: [] for epsilon in epsilons}

for epsilon in epsilons:

    print("\nrunning epsilon: ", epsilon)

    print("\nRunning Bin...")
    Bin(epsilon)
    print("\nRunning Mun...")
    Num(epsilon)
    print("\nRunning MunNum...")
    NumMun(epsilon)
    print("\nrunning NumMunUnb")
    NumMunUnb(epsilon)
    print("\nrunning NumMunUnbGeo")
    NumMunUnbGeo(epsilon)
    print("\nrunning NumMunUnbGeoLoc")
    NumMunUnbGeoLoc(epsilon)

    # Update the dataframes
    Bin_df = pd.read_csv('results/Bin_noisy_result.csv')
    Num_fil_df = pd.read_csv('results/Num_fil_noisy_result.csv')
    Num_df = pd.read_csv('results/Num_noisy_result.csv')
    NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')
    NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
    NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
    NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')

    # List of dataframes to process
    noisy_dfs = {
        "Bin_noisy": Bin_df,
        "Num_fil_noisy": Num_fil_df,
        "Num_noisy": Num_df,
        "NumMun_noisy": NumMun_df,
        "NumMunUnbGeoLoc_noisy": NumMunUnbGeoLoc_df,
        "NumMunUnbGeo_noisy": NumMunUnbGeo_df,
        "NumMunUnb_noisy": NumMunUnb_df
    }

    

    # Calculate differences for each dataframe and save to new CSV files
    for name, df in noisy_dfs.items():
        if 'HourDK' in df.columns:
            df.drop(columns=['HourDK'], inplace=True)
        df = convert_df_to_numeric(df)
        
        diff_df = calculate_differences(df)
        diff_df.to_csv(f'results/Synthetic/{name}_syn_epsilon={epsilon}_difference.csv', index=False)