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

Bin_df = pd.read_csv('results/Bin_noisy_result.csv')

Num_fil_df = pd.read_csv('results/Num_fil_noisy_result.csv')

Num_df = pd.read_csv('results/Num_noisy_result.csv')




# Pairing noisy and real dataframes
dataframe_pairs = [
    ('Bin', Bin_df, real_bin_df),
    ('Num', Num_df, real_num_df),
    ('Num_fil', Num_fil_df, real_num_fil_df),
]



# Parameters
epsilon = 1
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

#exp = np.exp(1)
exp = round(np.exp(1), 11)

# Loop over each dataframe
for name, noisy_df, real_df in dataframe_pairs:
    for s, row in real_df.iterrows():  # t is the index, row is the row data
        if s == 0:
            t = 1
        else:
            t = s

        for muni in real_df.columns:  # muni is each column, makes sense for NumMun, but works for all dataframes
            # Access values safely using .iloc to avoid index out of bounds
                noisy_t = noisy_df.iloc[t][muni]
                
                real_t = real_df.iloc[t][muni]
                real_t_minus_1 = real_df.iloc[t-1][muni]
                
                # Calculate probabilities assuming your noise model is correctly specified
                p_1 = 0.5 * np.exp(-(np.float64(noisy_t) - np.float64(real_t)))
                p_2 = 0.5 * np.exp(-(np.float64(noisy_t) - np.float64(real_t_minus_1)))
                
                # Compute the ratio of probabilities and compare it to exp(1)
                if p_2 == 0:  # Avoid division by zero
                    ratio = np.inf  # Set ratio to infinity if p_2 is zero
                else:
                    ratio = p_1 / p_2
                    ratio = round(ratio, 11)

                if ratio > exp:  
                    print(f"Ratio condition met for {muni} at time {t} in {name} with ratio: ", ratio, ">", exp)
                    print("np.float64(noisy_t): ", np.float64(noisy_t))
                    print("np.float64(real_t)", np.float64(real_t))
                    print("np.float64(real_t_minus_1)", np.float64(real_t_minus_1))
                    outliers[name].append((t, muni, ratio))
                #else:
                    #print("all good: ", t)
                    print("ratio: ", ratio, "<=", exp)
    print("df: ", name)


# Print the count of outliers for each DataFrame
for name, data in outliers.items():
    print(f"{name} - Total Outliers: {len(data)}")




