import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Experiment that shows the standard deviation of the differences 
# between the actual data and the result of NumMunUnbGeoLoc

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
result_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')

# Exclude first column (HourDK) in actual_df
actual_df = actual_df.drop(actual_df.columns[0], axis=1)

# Exclude first column (HourDK) in result_df
result_df = result_df.drop(result_df.columns[0], axis=1)

# Reorder columns of actual_df to match result_df
actual_df = actual_df[result_df.columns]

# Make a copy of the DataFrames
diff_df_copy = actual_df.copy()

# Find the average discrepancy of the actual and result DataFrames
def avg_discrepancy(actual_df, result_df):
    for i in actual_df.columns:
        for index, row in actual_df.iterrows():
            diff_df_copy.at[index, i] = abs(actual_df.at[index, i] - result_df.at[index, i])
    # Calculate the average of the differnces in dff_df_copy
    avg = diff_df_copy.mean(axis=0)
    return avg
                    
# Calculate the average discrepancy
avg_dis = avg_discrepancy(actual_df, result_df)

print("avg_dis: ", avg_dis)

# Plot the average deviation
plt.figure(figsize=(10, 6))
plt.plot(avg_dis.index, avg_dis.values, marker='o', linestyle='-')
plt.title('Average discrepancy between Actual and NumMunUnbGeoLoc')
plt.xlabel('Municipalities, Regions and DK')
plt.ylabel('Average deviation')
plt.grid(True)
plt.show()
