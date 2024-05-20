import pandas as pd
import matplotlib.pyplot as plt
from utils.load_dataset import load_dataset
from utils.clipData import clip

# Ensure to run the following files to generate needed CSV files:
# Generate_pure_dataset.py, NumMunUnbGeo.py, NumMunUnbGeoLoc.py

# Read the CSV file into a DataFrame
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

# Clip data with different thresholds
thresholds = [0.1, 0.5, 1, 2, 5]
clipped_dfs = [df_mun.copy() for _ in thresholds]

for df, thresh in zip(clipped_dfs, thresholds):
    df['ConsumptionkWh'], _ = clip(df, 'ConsumptionkWh', thresh)

# Pivot, compute cumulative sum, and drop rows with NaN values for each DataFrame
def pivot_cumsum_dropna(df):
    df_pivot = df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh').cumsum()
    return df_pivot.dropna()

df_mun = pivot_cumsum_dropna(df_mun)
clipped_dfs = [pivot_cumsum_dropna(df) for df in clipped_dfs]

print(df_mun)

# Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(df_list, label_list, muni):
    plt.figure()
    for df, label in zip(df_list, label_list):
        plt.plot(df[muni], label=label)
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframes: {label_list}')
    plt.show()

labels = ['df_mun'] + [f'clipped{thresh}' for thresh in thresholds]
for muni in [101, 825]:
    show_comparison_for_specific_muni([df_mun] + clipped_dfs, labels, muni)