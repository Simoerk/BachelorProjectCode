import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism2D import binary_mechanism_unbounded
from utils.clipData import clip
from utils.muniRegion import give_region
from utils.load_dataset import load_dataset
from utils.scale import downScale, upScale
import time

# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

#remove upper quantile
df_mun['ConsumptionkWh'], thresh = clip(df_mun, 'ConsumptionkWh')


#downscale
df_mun['ConsumptionkWh'], thresh = downScale(df_mun, 'ConsumptionkWh')
#min_val = 0
#max_val = thresh
#df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)

#Create result dataframe
result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times[1:]

#pivot such that the columns are the municipalities
df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')


# remove first row to account for uneven time intervals
df = df.iloc[1:]


#Calling the mechanism timed
start_time = time.time()
result_df = binary_mechanism_unbounded(1, df, result_df, 0.5)
end_time = time.time()

#Print the time
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")

#upscale
for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    result_df[col] = upScale(result_df, col, thresh)
    #result_df[col] = result_df[col] * (max_val - min_val) + min_val

#save to dataframe
result_df.to_csv("results/NumMunUnbGeo_noisy_result.csv", index=False)
print("done")


