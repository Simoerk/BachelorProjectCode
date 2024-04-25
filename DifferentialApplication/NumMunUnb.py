import numpy as np
import pandas as pd
import math
from Mechanisms.ModBinaryMechanism import mod_binary_mechanism
from utils.laplace import laplace_mechanism
from utils.clipData import clip
from utils.clipData import quantileSelection
from utils.muniRegion import give_region
from utils.load_dataset import load_dataset
import time




# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv", 1000000)



# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')


#remove upper quantile
df_mun['ConsumptionkWh'], thresh = clip(df_mun, 'ConsumptionkWh')


#scale
min_val = 0
max_val = thresh
df_mun['ConsumptionkWh'] = (df_mun['ConsumptionkWh'] - min_val) / (max_val - min_val)


result_df = pd.DataFrame()
unique_times = sorted(df_mun['HourDK'].unique())[1:]
result_df['HourDK'] = unique_times

mun_len = 0
i = 0


start_time = time.time()
for mun_no in df_mun['MunicipalityNo'].unique():

    # Filter the DataFrame for the current municipality
    mun_df = df_mun[df_mun['MunicipalityNo'] == mun_no]

    if i == 0:
        mun_len = len(mun_df)

    if len(mun_df) == mun_len:
        #remove first row to account for uneven time intervals
        mun_df = mun_df.iloc[1:]


    # Apply the binary mechanism for each municipality's data stream

    epsilon = 1  # Example epsilon value
    stream = mun_df['ConsumptionkWh'].tolist()

    # Call the binary mechanism function and store its list output
    alpha_hat = []

    B, alpha_hat, t_last = mod_binary_mechanism(epsilon, stream, alpha_hat, 0.5)
    

    # Calculate the difference in length between the two lists
    #length_difference = len(unique_times) - len(B)

    # Extend binary_results with NaN for the potential difference in length
    #binary_result = B + [np.nan] * length_difference
    
    # Add the results as a new column in the result DataFrame, named by the MunicipalityNo
    result_df[str(mun_no)] = B

    i+=1

end_time = time.time()

# Print the duration
duration = end_time - start_time
print(f"The function took {duration} seconds to run.")
    

# Scale back up
for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    result_df[col] = result_df[col] * (max_val - min_val) + min_val



# save the dataframe to a csv file
result_df.to_csv("results/NumMunUnb_noisy_result.csv", index=False)
print("done")