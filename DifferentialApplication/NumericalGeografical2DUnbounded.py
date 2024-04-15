import numpy as np
import pandas as pd
import math
from Mechanisms.modmodBinaryMechanism import binary_mechanism_unbounded
from utils.laplace import laplace_mechanism
from utils.clipData import clip
from utils.clipData import quantileSelection


def load_dataset(): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv("data/muni_data.csv") #, nrows=20000)
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



#scale
min_val = 0
max_val = thresh
df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)



result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times







result_df = binary_mechanism_unbounded(0.1, df_mun, result_df, 1)


#print(result_df)



for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    #print(result_df[col])
    result_df[col] = result_df[col] * (max_val - min_val) + min_val



print(result_df)
result_df.to_csv("results/result_unbound_Geo_df.csv", index=False)
print("done")