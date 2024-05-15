import pandas as pd
import numpy as np
from utils.scale import downScaleDf, upScaleDf, upScale, downScale
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo


def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df



# Parameters
epsilon = 1
theta = 0.5
delta = 0.001
num_runs = 3
intermediate_steps = False


real_df = pd.read_csv('results/regional_consumption_sums.csv')


# Initialize container for total outliers count
total_outliers = {'NumMunUnbGeo_df': 0, 'NumMunUnbGeoLoc_df': 0, "real_df": 0}

epsilon = 1


for _ in range(num_runs):

    print("running iteration: ", _)

    print("\nrunning NumMunUnbGeoLoc")
    NumMunUnbGeoLoc(epsilon)
    print("\nrunning NumMunUnbGeo")
    NumMunUnbGeo(epsilon)
 

    # Load datasets
    NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
    NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')



    NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, -6:]
    NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, -6:]
    real_df = real_df.iloc[:, -6:]



    # List of dataframes for processing
    dfs = [NumMunUnbGeo_df, NumMunUnbGeoLoc_df, real_df]
    #outliers = {name: [] for name in ['NumMunUnbGeo_df', 'NumMunUnbGeoLoc_df']}
    outliers = {name: [] for name in ['NumMunUnbGeo_df', 'NumMunUnbGeoLoc', "real_df"]}



    #Scale down. using global_max because we know the max is larger than the absolute of the smallest
    max_diffs = []
    real_df_num = dfs[2].apply(pd.to_numeric)
    for column in real_df_num.columns:
        # Calculate the absolute differences between consecutive rows
        differences = real_df_num[column].diff().abs()
        # Find the maximum difference in this column
        max_diff = differences.max()
        # Append the maximum difference to the list
        max_diffs.append(max_diff)

    # Find the global maximum difference across all columns and DataFrames
    global_max = max(max_diffs)




    for df in dfs:
        for column in df.columns:
            df[column] = (df[column] - 0) / (global_max - 0)



    # Loop over each dataframe
    for df_name, df in zip(outliers.keys(), dfs):
        for t, row in df.iterrows():  # t is the index of row
            # Skip the first row since log(1) = 0, which would cause the threshold to be 0
            if t == 0:
                bound = ((1 / (theta * epsilon)) * ((np.log2(t + 2))**(1.5+theta)) * np.log2(1 / delta))
            else:
                bound = ((1 / (theta * epsilon)) * ((np.log2(t + 1))**(1.5+theta)) * np.log2(1 / delta))
            for muni in df.columns:  # muni is each column
                real_value = dfs[2].at[t, muni]
                noisy_value = row[muni]
                if not np.abs((real_value) - (noisy_value)) <= bound:
                    outliers[df_name].append((muni, t))
                    print("muni: ", muni)
                    print("t: ", t)
                    print("real_value: ", real_value)
                    print("noisy_value: ", noisy_value)
                    print("bound: ", bound)
                    print("real-noisy: ", np.abs(np.float64(real_value) - np.float64(noisy_value)))    

    if intermediate_steps:
        # Print the count of outliers for each DataFrame
        for df_name, municipality_data in outliers.items():
            print(f"{df_name} - Total Outliers: {len(municipality_data)}")




# Calculate averages
average_outliers = {key: value / num_runs for key, value in total_outliers.items()}

# Print the results
for df_name, avg in average_outliers.items():
    print(f"{df_name} - Average Total Outliers: {avg:.2f}")
