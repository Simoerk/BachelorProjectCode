import pandas as pd
import numpy as np
from utils.scale import downScaleDf, upScaleDf, upScale, downScale

def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


# Load datasets
real_bin_df = pd.read_csv('results/Bin_result.csv')
real_num_df = pd.read_csv('results/Num_result.csv')
real_nummun_df = pd.read_csv('results/NumMun_result.csv')
Bin_df = pd.read_csv('results/Bin_noisy_result.csv')
Num_df = pd.read_csv('results/Num_noisy_result.csv')
NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')




# Parameters
epsilon = 1
delta = 0.001


# List of dataframes for processing
dfs = [real_bin_df, real_num_df, real_nummun_df, Bin_df, Num_df, NumMun_df]
outliers = {name: [] for name in ['Bin', 'Num' 'NumMun',]}



#delete first column of all dfs
dfs = [df.drop(columns=['HourDK']) for df in dfs]

# Reorder columns of df2 to match df1
#dfs = [df.reindex(columns=real_df.columns) for df in dfs]


#Scale down. using global_max because we know the max is larger than the absolute of the smallest
max_diffs = []
real_df_num = dfs[4].apply(pd.to_numeric)
for column in real_df_num.columns:
    # Calculate the absolute differences between consecutive rows
    differences = real_df_num[column].diff().abs()
    # Find the maximum difference in this column
    max_diff = differences.max()
    # Append the maximum difference to the list
    max_diffs.append(max_diff)

# Find the global maximum difference across all columns and DataFrames
global_max = max(max_diffs)



for df in dfs:
    for column in df.columns:
        df[column] = (df[column] - 0) / (global_max - 0)



# Loop over each dataframe
for df_name, df in zip(outliers.keys(), dfs):
    for t, row in df.iterrows():  # t is the index of row
        # Skip the first row since log(1) = 0, which would cause the threshold to be 0
        if t == 0:
            bound = ((1 / (theta * epsilon)) * ((np.log2(t + 2))**(1.5+theta)) * np.log2(1 / delta))
        else:
            bound = ((1 / (theta * epsilon)) * ((np.log2(t + 1))**(1.5+theta)) * np.log2(1 / delta))
        for muni in df.columns:  # muni is each column
            real_value = dfs[4].at[t, muni]
            noisy_value = row[muni]
            if not np.abs((real_value) - (noisy_value)) <= bound:
                outliers[df_name].append((muni, t))
                print("muni: ", muni)
                print("t: ", t)
                print("real_value: ", real_value)
                print("noisy_value: ", noisy_value)
                print("bound: ", bound)
                print("real-noisy: ", np.abs(np.float64(real_value) - np.float64(noisy_value)))

# Print the count of outliers for each DataFrame
for df_name, municipality_data in outliers.items():
    print(f"{df_name} - Total Outliers: {len(municipality_data)}")




