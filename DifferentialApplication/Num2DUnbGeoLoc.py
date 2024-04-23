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
from utils.load_dataset import load_dataset
import time
#from utils.visualizeData import visualize_data


# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

#remove upper quantile
#df_mun['ConsumptionkWh'] = clip(df_mun, 'ConsumptionkWh')
#with open("./data/threshold.txt", 'r') as file:
    #thresh = float(file.read())

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

#Calling the mecchanism timed
start_time = time.time()
result_df, thresh_df = binary_mechanism_unbounded_local(0.1, df, result_df, 1, 1, thresh_df)
end_time = time.time()

#print the time it took to run
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")

#Upscaling
result_df = upScaleDf(result_df, thresh_df)


result_df.to_csv("results/Num2DUnbGeoLoc_noisy_result.csv", index=False)
print("done")




