import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
result_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')

# Exclude first column (HourDK) in actual_df
actual_df = actual_df.drop(actual_df.columns[0], axis=1)

# Exclude first column (HourDK) in result_df
result_df = result_df.drop(result_df.columns[0], axis=1)

# Reorder columns of actual_df to match result_df
actual_df = actual_df[result_df.columns]

# Summary statistics for actual dataset
actual_summary = actual_df.describe()

# Summary statistics for noisy dataset
noisy_summary = result_df.describe()

# Compare summary statistics
summary_comparison = pd.concat([actual_summary, noisy_summary], axis=1, keys=['Actual', 'Noisy'])
print(summary_comparison)

# Visualize distribution of electricity consumption for each municipality
plt.figure(figsize=(12, 6))
actual_df.boxplot(column=list(actual_df.columns))
plt.title('Boxplot of Electricity Consumption by Municipality (Actual)')
plt.ylabel('Electricity Consumption')
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(12, 6))
result_df.boxplot(column=list(result_df.columns))
plt.title('Boxplot of Electricity Consumption by Municipality (Noisy)')
plt.ylabel('Electricity Consumption')
plt.xticks(rotation=45)
plt.show()