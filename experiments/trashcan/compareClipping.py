import pandas as pd
import matplotlib.pyplot as plt
from utils.load_dataset import load_dataset
from utils.clipData import clip

# Ensure to run the following files to generate needed CSV files:
# Generate_pure_dataset.py, NumMunUnbGeo.py, NumMunUnbGeoLoc.py

# Read the CSV file into a DataFrame
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Ensure MunicipalityNo is of type string
df_mun['MunicipalityNo'] = df_mun['MunicipalityNo'].astype(str)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

# Clip data with different thresholds
epsilons = [0.1, 0.5, 1, 2, 5]
clipped_dfs = [df_mun.copy() for _ in epsilons]

for df, epsilon in zip(clipped_dfs, epsilons):
    df['ConsumptionkWh'], _ = clip(df, 'ConsumptionkWh', epsilon)

# Pivot the original and clipped dataframes
df_mun = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
df_mun = df_mun.iloc[1:]
df_mun = df_mun.cumsum()

for i, df in enumerate(clipped_dfs):
    df = df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    df = df.iloc[1:]
    df = df.cumsum()
    clipped_dfs[i] = df  # Ensure the modified DataFrame is assigned back

# Show comparison between actual and local noisy data for a specific municipality
def show_comparison_for_specific_muni(df_list, label_list, muni):
    plt.figure()
    for df, label in zip(df_list, label_list):
        if str(muni) in df.columns:
            plt.plot(df[str(muni)], label=label)
        else:
            print(f"Municipality {muni} not found in DataFrame with label {label}.")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframes: {label_list}')
    plt.show()

# Show the comparison for a specific municipality
labels = ['df_mun'] + [f'clipped{epsilon}' for epsilon in epsilons]
for muni in [101, 825]:
    show_comparison_for_specific_muni([df_mun] + clipped_dfs, labels, muni)
