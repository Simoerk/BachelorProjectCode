import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism2DLocal import binary_mechanism_unbounded_local
from utils.clipData import *
from utils.scale import downScaleDf
from utils.scale import upScaleDf
from utils.load_dataset import load_dataset
import time



# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')



# create the result df
result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())
result_df['HourDK'] = unique_times[1:]

# pivot to make the municipalities the columns
df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

# remove first row to account for uneven time intervals
df = df.iloc[1:]

# clip the data
df_mun = clip_pr_column(df)

#Downscaling
df, thresh_df = downScaleDf(df)

#Calling the mecchanism timed
start_time = time.time()
result_df, thresh_df = binary_mechanism_unbounded_local(2, df, result_df, 0.5, thresh_df)
end_time = time.time()

#print the time it took to run
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")

#Upscaling
result_df = upScaleDf(result_df, thresh_df)

#save to csv file
result_df.to_csv("results/NumMunUnbGeoLoc_noisy_result.csv", index=False)
print("done")




