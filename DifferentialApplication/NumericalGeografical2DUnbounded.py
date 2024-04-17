import numpy as np
import pandas as pd
import math
from Mechanisms.modmodBinaryMechanism import binary_mechanism_unbounded
from utils.laplace import laplace_mechanism
from utils.clipData import clip
from utils.clipData import quantileSelection
from utils.muniRegion import give_region
#from utils.visualizeData import visualize_data


def load_dataset(): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv("data/muni_data.csv")#, nrows=500000)
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


#count number of munies
municipality_counts = df_mun['MunicipalityNo'].value_counts()




#Test to find the actual aggregated data for 101
sum_consumption_101 = df_mun[df_mun['MunicipalityNo'] == 101]['ConsumptionkWh'].sum()
print(f"Sum of ConsumptionkWh for MunicipalityNo 101: {sum_consumption_101}")





#df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
#print(df)
#visualize_data(df)




#scale
min_val = 0
max_val = thresh
df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)



result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times[1:]





result_df = binary_mechanism_unbounded(0.1, df_mun, result_df, 1, 1, unique_times)
#result_df, mun = binary_mechanism_unbounded(0.1, df_mun, result_df, 1, 1, unique_times)


for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    result_df[col] = result_df[col] * (max_val - min_val) + min_val



result_df.to_csv("results/result_unbound_Geo_df.csv", index=False)
print("done")




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

