import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
result_df = pd.read_csv('results/Num2DUnbGeoLoc_noisy_result.csv')

# Extract relevant columns (municipality numbers)
municipalities_result = result_df.columns[1:]  # Exclude first column (HourDK)

# Reorder columns of df2 to match df1
actual_df = actual_df.reindex(columns=municipalities_result)

# Make a copy of the DataFrames
diff_df_copy = actual_df.copy()

# Calculate the standard deviation of the differences between the actual and result DataFrames
def std_deviation(actual_df, result_df):
    # Calculate the absolute difference between corresponding elements of actual_df and result_df
    std_df = actual_df.sub(result_df).abs()
    
    # Calculate the standard deviation of the differences for each column
    std_dev = std_df.std()

    return std_dev

# Find the average discrepancy of the actual and result DataFrames
def avg_discrepancy(actual_df, result_df):
    for i in actual_df.columns:
        for index, row in actual_df.iterrows():
            diff_df_copy.at[index, i] = abs(actual_df.at[index, i] - result_df.at[index, i])
    # Calculate the average of the differnces in std_df_copy
    avg = diff_df_copy.mean(axis=0)
    return avg
                    
# Calculate the average discrepancy
avg_dis = avg_discrepancy(actual_df, result_df)

# Calculate the standard deviation of the differences
std_dev = std_deviation(actual_df, result_df)

# Plot the average discrepancy
plt.figure(figsize=(10, 6))
plt.plot(avg_dis.index, avg_dis.values, marker='o', linestyle='-')
plt.title('Average discrepancy of Actual and Result DataFrames')
plt.xlabel('Municipality Number')
plt.ylabel('Average discrepancy')
plt.grid(True)
plt.show()

# Plot the standard deviation of the differences
plt.figure(figsize=(10, 6))
plt.plot(std_dev.index, std_dev.values, marker='o', linestyle='-')
plt.title('Standard deviation of the differences between Actual and Result DataFrames')
plt.xlabel('Municipality Number')
plt.ylabel('Standard deviation')
plt.grid(True)
plt.show()