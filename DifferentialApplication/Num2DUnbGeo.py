import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism2D import binary_mechanism_unbounded
from utils.laplace import laplace_mechanism
from utils.clipData import clip
from utils.clipData import quantileSelection
from utils.muniRegion import give_region
#from utils.visualizeData import visualize_data
from utils.load_dataset import load_dataset
import time

# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

#Test to find the actual aggregated data for 101
sum_consumption_101 = df_mun[df_mun['MunicipalityNo'] == 101]['ConsumptionkWh'].sum()
print(f"Sum of ConsumptionkWh for MunicipalityNo 101: {sum_consumption_101}")

#remove upper quantile
df_mun['ConsumptionkWh'], thresh = clip(df_mun, 'ConsumptionkWh')


#scale
min_val = 0
max_val = max(df_mun['ConsumptionkWh'])
df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)

result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times[1:]

df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')


#This is to make a csv file
df = df.iloc[1:]
df.insert(0, 'HourDK', unique_times[1:])
df.to_csv("results/processed_data.csv", index=False)
df = df.drop('HourDK', axis=1)

#Calling the mechanism timed
start_time = time.time()
result_df = binary_mechanism_unbounded(0.1, df, result_df, 1, 1, unique_times)
end_time = time.time()

#Print the time
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")


for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    result_df[col] = result_df[col] * (max_val - min_val) + min_val

result_df.to_csv("results/Num2DUnbGeo_noisy_result.csv", index=False)
print("done")





# Beneath this line is for some tests
def accumulate_regional_values(result_df):
    regional_values = {
        "Hovedstaden": 0.0,
        "Sjaelland": 0.0,
        "Syddanmark": 0.0,
        "Midtjylland": 0.0,
        "Nordjylland": 0.0
    }

    region_dict = give_region()

    # Iterate over each municipality number and its corresponding region
    for muni_number, region in region_dict.items():
        # Ensure the municipality number is a column in result_df
        regional_values[region] += result_df[int(muni_number)].iloc[-1]

    return regional_values

regional_sums = accumulate_regional_values(result_df)

