import pandas as pd
import numpy as np

def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


# Load datasets
real_df = pd.read_csv('results/real_consumption_sums.csv')
NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')

# Adjust columns as needed (assuming you've trimmed the last 6 columns correctly)
real_df = convert_df_to_numeric(real_df)
NumMunUnbGeoLoc_df = convert_df_to_numeric(NumMunUnbGeoLoc_df.iloc[:, :-6])
NumMunUnbGeo_df = convert_df_to_numeric(NumMunUnbGeo_df.iloc[:, :-6])
NumMunUnb_df = convert_df_to_numeric(NumMunUnb_df)
NumMun_df = convert_df_to_numeric(NumMun_df)

# Parameters
epsilon = 1
theta = 0.5
delta = 0.001

# List of dataframes for processing
dfs = [NumMun_df, NumMunUnb_df, NumMunUnbGeo_df, NumMunUnbGeoLoc_df]
outliers = {name: [] for name in ['NumMun', 'NumMunUnb', 'NumMunUnbGeo', 'NumMunUnbGeoLoc']}

# Loop over each dataframe
for df_name, df in zip(outliers.keys(), dfs):
    for t, row in df.iterrows():  # t is the index of row
        for muni in df.columns:  # muni is each column
            real_value = real_df.at[t, muni]
            noisy_value = row[muni]
            threshold = (1 / (theta * epsilon)) * np.log2(t + 1) * np.log2(1 / delta)

            if not np.abs(real_value - noisy_value) < threshold:
                outliers[df_name].append((muni, t))

# Print results
for key, value in outliers.items():
    print(f"Outliers in {key}: {value}")
