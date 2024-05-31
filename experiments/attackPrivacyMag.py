import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

noisy_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')

def calculate_noisy_original_values(noisy_df):
    # Exclude the 'HourDK' column from the calculation
    numeric_df = noisy_df.drop(columns=['HourDK'])
    
    # Calculate the differences between consecutive rows for each numeric column to get the original values
    noisy_original_values = numeric_df.diff().dropna().reset_index(drop=True)
    
    # Re-add the 'HourDK' column
    noisy_original_values['HourDK'] = noisy_df['HourDK'].iloc[1:].reset_index(drop=True)
    
    return noisy_original_values

def scale_values(df):
    # Exclude the 'HourDK' column from the scaling
    columns_to_scale = df.drop(columns=['HourDK'])
    
    # Find the minimum and maximum values in the DataFrame
    min_val = columns_to_scale.min().min()
    max_val = columns_to_scale.max().max()
    
    # Scale the values to the range [0, 1]
    scaled_df = (columns_to_scale - min_val) / (max_val - min_val)
    
    # Re-add the 'HourDK' column
    scaled_df['HourDK'] = df['HourDK']
    
    return scaled_df


# Function to compute the CDF for the entire dataset
def compute_cdf(df):

    # Flatten the DataFrame values into a single array
    data_values = df.drop(columns=['HourDK']).values.flatten()
    
    # Sort the data values
    sorted_data = np.sort(data_values)
    
    # Compute the CDF values
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    return sorted_data, cdf

# Function to infer if a value is high or low based on the CDF
def infer_value(value, sorted_data, cdf, highthreshold=0.9, lowthreshold=0.1):

    # Find the CDF value corresponding to the given value
    idx = np.searchsorted(sorted_data, value, side="right") - 1
    if idx < 0:
        idx = 0
    cdf_value = cdf[idx]
    
    # Classify based on the threshold
    if cdf_value > highthreshold:
        return 'High'
    elif cdf_value < lowthreshold:
        return 'Low'
    else:
        return 'Medium'


# Use the function to calculate the noisy original values
noisy_original_values = calculate_noisy_original_values(noisy_df)

# Use the function to scale the values
scaled_noisy_original_values = scale_values(noisy_original_values)

sorted_data, cdf = compute_cdf(scaled_noisy_original_values)

# Test the inference function
test_value = 0.75
inference = infer_value(test_value, sorted_data, cdf)
print(f'The value {test_value} is inferred as {inference}')


# Plot the CDF
plt.figure(figsize=(10, 6))
plt.plot(sorted_data, cdf, marker='.', linestyle='none')
plt.xlabel('Data Value')
plt.ylabel('CDF')
plt.title('CDF of Scaled Noisy Original Values')
plt.grid(True)
plt.show()

