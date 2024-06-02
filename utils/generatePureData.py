from utils.clipData import *
from utils.loadDataset import load_dataset

# Util to make a dataset with a cumulative sum of the real consumption data from Energinet

# Load dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh, removing categories
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

unique_times = sorted(df_mun['HourDK'].unique())

# Pivot to make it so that municipalities represent the columns
df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

# Remove first row to account for uneven time intervals in the dataset
df = df.iloc[1:]

# Make the data a cumulative sum
df = df.cumsum()

# Make processed csv file MÅSKe fJERN?
df.insert(0, 'HourDK', unique_times[1:])

# Save to csv file
df.to_csv("results/real_consumption_sums.csv", index=False)
print("done")

