import pandas as pd
import numpy as np
from utils.scale import downScaleDf, upScaleDf, upScale, downScale
import math

def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


# Load datasets
real_bin_df = pd.read_csv('results/Bin_result.csv')

real_num_fil_df  = pd.read_csv('results/num_fil_result.csv')

real_num_df = pd.read_csv('results/num_result.csv')

real_nummun_df = pd.read_csv('results/real_consumption_sums.csv')

Bin_df = pd.read_csv('results/Bin_noisy_result.csv')

Num_fil_df = pd.read_csv('results/Num_fil_noisy_result.csv')

Num_df = pd.read_csv('results/Num_noisy_result.csv')

NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')


# Pairing noisy and real dataframes
dataframe_pairs = [
    ('Bin', Bin_df, real_bin_df),
    ('Num', Num_df, real_num_df),
    ('Num_fil', Num_fil_df, real_num_fil_df),
    ('NumMun', NumMun_df, real_nummun_df)
]



# Parameters
epsilon = 1
delta = 0.001
B = 504

for name, noisy_df, real_df in dataframe_pairs:
    if 'HourDK' in real_df.columns:
        noisy_df.drop(columns=['HourDK'], inplace=True)
        real_df.drop(columns=['HourDK'], inplace=True)

    # Convert columns to numeric
    noisy_df = noisy_df.apply(pd.to_numeric, errors='coerce')
    real_df = real_df.apply(pd.to_numeric, errors='coerce')

    # Calculate the absolute differences and find the maximum difference
    max_diff = real_df.diff().abs().max().max()
    

    for column in real_df.columns:
        # Scale both dataframes by the maximum difference
        noisy_df[column] = noisy_df[column] / max_diff
        real_df[column] = real_df[column] / max_diff

    # To ensure changes are reflected outside the loop or in the original list, update the dataframes in the list:
    index = next(i for i, pair in enumerate(dataframe_pairs) if pair[0] == name)
    dataframe_pairs[index] = (name, noisy_df, real_df)

        
        


outliers = {name: [] for name, _, __ in dataframe_pairs}


# Loop over each dataframe
for name, noisy_df, real_df in dataframe_pairs:
    for s, row in real_df.iterrows():  # t is the index, row is the row data
        if s == 0:
            t = 1
        else:
            t = s

        for muni in real_df.columns:  # muni is each column, makes sense for NumMun, but works for all dataframes
            real_value = row[muni]
            noisy_value = noisy_df.at[t, muni]

            # Check the specific dataframe and set the bound
            if name == 'Bin': #B = sqrt(T), so approx T^0.25 = 12 errors with 0.001 prob
                bound = (1 / epsilon) * np.sqrt(((t+1) / B) + B) * np.log(1 / delta)
            elif name == 'NumMun':
                T = 1099 # T = 1099 approx 1 errors
                bound = (1 / epsilon) * np.log(T) * np.sqrt(np.log(t+1)) * np.log(1 / delta)
            else:
                T = 27048 #T=27048 approx 27 errrors
                bound = (1 / epsilon) * np.log(T) * np.sqrt(np.log(t+1)) * np.log(1 / delta)

            # Outlier detection
            if not np.abs(real_value - noisy_value) <= bound:
                outliers[name].append((muni, t))
                print(f"\nmuni: {muni}, t: {t}, real_value: {real_value}, noisy_value: {noisy_value}, bound: {bound}")
                print(f"real-noisy difference: {np.abs(np.float64(real_value) - np.float64(noisy_value))}")
            else:
                print("bound: ", bound, " value: ", np.abs(real_value - noisy_value) )




# Print the count of outliers for each DataFrame
for name, data in outliers.items():
    print(f"{name} - Total Outliers: {len(data)}")



