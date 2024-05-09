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


# Pairing noisy and real dataframes
dataframe_pairs = [
    ('Bin', Bin_df, real_bin_df),
    ('Num', Num_df, real_num_df),
    ('NumMun', NumMun_df, real_nummun_df)
]



# Parameters
epsilon = 1
delta = 0.001


for name, noisy_df, real_df in dataframe_pairs:
    if name in ['Num', 'NumMun']:
        # Remove 'HourDK' from NumMun
        if 'HourDK' in noisy_df.columns:
            noisy_df.drop(columns=['HourDK'], inplace=True)
            real_df.drop(columns=['HourDK'], inplace=True)

        # Convert columns to numeric, find global maximum, and scale
        noisy_df = noisy_df.apply(pd.to_numeric, errors='coerce')
        real_df = real_df.apply(pd.to_numeric, errors='coerce')
        max_val_noisy = noisy_df.max().max()
        max_val_real = real_df.max().max()
        global_max = max(max_val_noisy, max_val_real)

        noisy_df /= global_max
        real_df /= global_max




outliers = {name: [] for name, _, __ in dataframe_pairs}

for name, noisy_df, real_df in dataframe_pairs:
    for t, (noisy_row, real_row) in enumerate(zip(noisy_df.iterrows(), real_df.iterrows())):
        index, noisy_data = noisy_row
        _, real_data = real_row
        for muni in noisy_data.index:  # Assuming muni is the column name
            real_value = real_data[muni]
            noisy_value = noisy_data[muni]
            if t == 0:
                continue  # Skip first row to avoid log(0)
            bound = ((1 / (epsilon)) * ((np.log2(t + 1))**(1.5+0.5)) * np.log2(1 / delta))
            if not np.abs(real_value - noisy_value) <= bound:
                outliers[name].append((muni, t))

# Print the count of outliers for each DataFrame
for name, data in outliers.items():
    print(f"{name} - Total Outliers: {len(data)}")


# Print the count of outliers for each DataFrame
for name, data in outliers.items():
    print(f"{name} - Total Outliers: {len(data)}")



