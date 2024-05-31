import numpy as np
import pandas as pd
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

# Set the epsilon value
epsilon = 1

# Function for clipping all data in the dataset
def global_clip():

    # Find the total amount of consumption in the dataset
    total_consumption_before_global = df_mun["ConsumptionkWh"].sum()

    # Clip the data
    df_mun['ConsumptionkWh'], global_thresh = clip(df_mun, 'ConsumptionkWh', epsilon)

    # Pivot to make the municipalities represent the columns
    actual_global_df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    # Remove first row to account for uneven time intervals
    actual_global_df = actual_global_df.iloc[1:]

    # Count the number of values in the dataframe equal to the threshold
    count = 0
    for column in actual_global_df.columns:
        for index in actual_global_df.index:
            if actual_global_df[column][index] == global_thresh:
                count += 1

    # Find the total amount of consumption removed from the dataset after global clipping
    total_consumption_after_global = 0
    for column in actual_global_df.columns:
        total_consumption_after_global += actual_global_df[column].sum()

    removed_consumption_global = total_consumption_before_global - total_consumption_after_global

    return count, removed_consumption_global

# Function for clipping the data per column, i.e. per municipality
def local_clip():

    # Pivot to make the municipalities the columns
    df = df_mun_2.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    
    # Remove first row to account for uneven time intervals
    df = df.iloc[1:]

    # Find the total amount of consumption in the dataset
    total_consumption_before_local = 0
    for column in df.columns:
        total_consumption_before_local += df[column].sum()


    # Clip the data locally per column, i.e. per municipality
    actual_local_df, local_thresh_list = clip_pr_column(df, epsilon)

    # Count the number of values in the dataframe equal to the threshold
    count = 0
    for column, local_thresh in zip(actual_local_df.columns, local_thresh_list):
        for index in actual_local_df.index:
            if actual_local_df[column][index] == local_thresh:
                count += 1
    
    # Find the total amount of consumption removed from the dataset after global clipping
    total_consumption_after_local = 0
    for column in actual_local_df.columns:
        total_consumption_after_local += actual_local_df[column].sum()

    removed_consumption_local = total_consumption_before_local - total_consumption_after_local

    return count, removed_consumption_local

# Initialize lists to store the results of counts and removed consumption
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

# Calculate the mean of the results
global_count = np.mean(global_count_list)
removed_consumption_global = np.mean(removed_consumption_global_list)

local_count = np.mean(local_count_list)
removed_consumption_local = np.mean(removed_consumption_local_list)

# Print the results
print(f"Global count: {global_count}")
print(f"Removed consumption global: {removed_consumption_global}")
print(f"Local count: {local_count}")
print(f"Removed consumption local: {removed_consumption_local}")
