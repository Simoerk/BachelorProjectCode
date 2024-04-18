import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism2DLocal import binary_mechanism_unbounded_local
from utils.laplace import laplace_mechanism
from utils.clipData import *
from utils.clipData import quantileSelection
from utils.muniRegion import give_region
from utils.scale import downScaleDf
from utils.scale import upScaleDf
#from utils.visualizeData import visualize_data

def load_dataset(): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv("data/muni_data.csv", nrows=1000000)
    print("Dataset loaded successfully!")
    return data

# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset()

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

#remove upper quantile
df_mun['ConsumptionkWh'] = clip(df_mun, 'ConsumptionkWh')
with open("./data/threshold.txt", 'r') as file:
    thresh = float(file.read())

df_mun = clip_pr_column(df_mun)



#Test to find the actual aggregated data for 101
sum_consumption_101 = df_mun[df_mun['MunicipalityNo'] == 101]['ConsumptionkWh'].sum()
print(f"Sum of ConsumptionkWh for MunicipalityNo 101: {sum_consumption_101}")
sum_consumption_825 = df_mun[df_mun['MunicipalityNo'] == 825]['ConsumptionkWh'].sum()
print(f"Sum of ConsumptionkWh for MunicipalityNo 825: {sum_consumption_825}")

#visualize ting
#df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
#print(df)
#visualize_data(df)

# #scale
# min_val = 0
# max_val = thresh
# df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)

result_df = pd.DataFrame()


#måske fjern
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times[1:]


df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

#Make processed csv file
df = df.iloc[1:]

#Make processed csv file MÅSKe fJERN?
df.insert(0, 'HourDK', unique_times[1:])
df.to_csv("results/processed_data.csv", index=False)
df = df.drop('HourDK', axis=1)

aggregated_consumption = [df[municipality].sum() for municipality in df.columns]
aggregated_df = pd.DataFrame([aggregated_consumption], columns=df.columns)
aggregated_df.to_csv("results/processed_sums_data.csv", index=False)

#Downscaling
df, thresh_df = downScaleDf(df)



result_df, thresh_df = binary_mechanism_unbounded_local(0.1, df, result_df, 1, 1, thresh_df)
#result_df, mun = binary_mechanism_unbounded(0.1, df_mun, result_df, 1, 1, unique_times)

# for col in result_df.columns[1:]:  # Skip the first column (time)
#     # Scale back each column to its original range
#     result_df[col] = result_df[col] * (max_val - min_val) + min_val

#Upscaling
result_df = upScaleDf(result_df, thresh_df)


result_df.to_csv("results/result_Num2DGeoLocal_df.csv", index=False)
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

