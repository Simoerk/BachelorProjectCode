import numpy as np
import pandas as pd
import math
import time
from utils.clipData import clip_pr_column
from utils.clipData import clip
from utils.load_dataset import load_dataset

# Load the dataset
df_mun = load_dataset("data/muni_data.csv", 1000000)

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

# Copy the dataset
df_mun_2 = df_mun.copy()

# Find the largest value in df_mun["ConsumptionkWh"]
max_val = df_mun["ConsumptionkWh"].max()
print(f"Max value: {max_val}")

# Find the largest value in df_mun["MunicipalityNo = 101"]
max_val_101 = df_mun[df_mun["MunicipalityNo"] == 101]["ConsumptionkWh"].max()
print(f"Max value 101: {max_val_101}")

# Set the privacy budget
epsilon = 1

# Globally clip the data
def global_clip():
    #find the total amount of consumption in the dataset
    total_consumption_before = df_mun['ConsumptionkWh'].sum()

    #clip the data
    df_mun['ConsumptionkWh'], global_thresh = clip(df_mun, 'ConsumptionkWh', epsilon)

    #print(f"Global thresh: {global_thresh}")

    actual_global_df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    #remove first row to account for uneven time intervals
    actual_global_df = actual_global_df.iloc[1:]

    #count the number of values in the dataframe equal to the threshold
    count = 0
    for column in actual_global_df.columns:
        for index in actual_global_df.index:
            if actual_global_df[column][index] == global_thresh:
                count += 1

    #find the total amount of consumption removed from the dataset after global clipping
    total_consumption_after = 0
    for column in actual_global_df.columns:
        total_consumption_after += actual_global_df[column].sum()

    removed_consumption = total_consumption_before - total_consumption_after

    return count, removed_consumption
    


# Locally clip the data
def local_clip():
    #find the total amount of consumption in the dataset
    total_consumption_before = df_mun_2['ConsumptionkWh'].sum()

    #pivot to make the municipalities the columns
    df = df_mun_2.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    
    # remove first row to account for uneven time intervals
    df = df.iloc[1:]

    # clip the data
    actual_local_df, local_thresh_list = clip_pr_column(df, epsilon)

    #count the number of values in the dataframe equal to the threshold
    count = 0
    for column, local_thresh in zip(actual_local_df.columns, local_thresh_list):
        #print(f"Local thresh: {local_thresh}")
        for index in actual_local_df.index:
            if actual_local_df[column][index] == local_thresh:
                count += 1
    
    #find the total amount of consumption removed from the dataset after global clipping
    total_consumption_after = 0
    for column in actual_local_df.columns:
        total_consumption_after += actual_local_df[column].sum()

    removed_consumption = total_consumption_before - total_consumption_after

    return count, removed_consumption


global_count_list = []
removed_consumption_global_list = []

local_count_list = []
removed_consumption_local_list = []

# Run the global and local clipping
for _ in range(10):
    global_count, removed_consumption_global = global_clip()
    global_count_list.append(global_count)
    removed_consumption_global_list.append(removed_consumption_global)

for _ in range(10):
    local_count, removed_consumption_local = local_clip()
    local_count_list.append(local_count)
    removed_consumption_local_list.append(removed_consumption_local)

global_count = np.mean(global_count_list)
removed_consumption_global = np.mean(removed_consumption_global_list)

local_count = np.mean(local_count_list)
removed_consumption_local = np.mean(removed_consumption_local_list)

print(f"Global count: {global_count}")
print(f"Removed consumption global: {removed_consumption_global}")
print(f"Local count: {local_count}")
print(f"Removed consumption local: {removed_consumption_local}")
