import numpy as np
import pandas as pd
import math
from Mechanisms.ModBinaryMechanism import Binary_tree_mechanism
from utils.laplace import laplace_mechanism
from utils.clipData import clip
from utils.clipData import quantileSelection


def load_dataset(): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv("data/muni_data.csv")
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


for mun_no in df_mun['MunicipalityNo'].unique():

    # Filter the DataFrame for the current municipality
    mun_df = df_mun[df_mun['MunicipalityNo'] == mun_no]
    
    # Apply the binary mechanism for each municipality's data stream

    epsilon = 0.1  # Example epsilon value
    stream = mun_df['ConsumptionkWh'].tolist()

    # Call the binary mechanism function and store its list output
    alpha_hat = []
    t_last = 1

    B, alpha_hat, t_last = Binary_tree_mechanism(epsilon, stream, alpha_hat, t_last)
    

    # Calculate the difference in length between the two lists
    length_difference = len(unique_times) - len(B)

    # Extend binary_results with NaN for the potential difference in length
    binary_result = B + [np.nan] * length_difference
    
    # Add the results as a new column in the result DataFrame, named by the MunicipalityNo
    result_df[str(mun_no)] = binary_result

    


for col in result_df.columns[1:]:  # Skip the first column (time)
    # Scale back each column to its original range
    result_df[col] = result_df[col] * (max_val - min_val) + min_val




result_df.to_csv("results/result_unbound_df.csv", index=False)
print("done")