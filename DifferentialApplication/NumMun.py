import numpy as np
import pandas as pd
from Mechanisms.BinaryMechanism import binary_mechanism
from utils.clipData import clip
from utils.load_dataset import load_dataset
from utils.scale import downScale, upScale
import time
from utils.muniRegion import *

# NumMun(epsilon) applies the binary mechanism to the electricity dataset from Energinet
def NumMun(epsilon):

    # To preserve epsilon differential privacy because two epsilon differential privacy mechanisms are called
    epsilon = epsilon/2

    # Load dataset with Municipality, time and housing/heating category
    df_mun = load_dataset("data/muni_data.csv", 1000000)

    # Group by HourDK and MunicipalityNo and sum the ConsumptionkWh, removing categories
    df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

    # Remove upper quantile with the clipping method
    df_mun['ConsumptionkWh'], thresh = clip(df_mun, 'ConsumptionkWh', epsilon)

    # Downscale
    df_mun['ConsumptionkWh'], thresh = downScale(df_mun, 'ConsumptionkWh')

    # Find unique timestamps and create result dataframe
    result_df = pd.DataFrame()
    unique_times = sorted(df_mun['HourDK'].unique())[1:]
    result_df['HourDK'] = unique_times

    mun_len = 0
    i = 0

    # Used for timing the mechanism loop
    start_time = time.time()

    # Loop through each unique MunicipalityNo 
    for mun_no in df_mun['MunicipalityNo'].unique():

        # Filter the DataFrame for the current municipality
        mun_df = df_mun[df_mun['MunicipalityNo'] == mun_no]

        # Get the length of the first municipality
        if i == 0:
            mun_len = len(mun_df)

        # Remove the first row to account for uneven time intervals in the dataset
        if len(mun_df) == mun_len:
            mun_df = mun_df.iloc[1:]

        # Get the consumption values as a list
        stream = mun_df['ConsumptionkWh'].tolist()
        # Get the length of the stream
        T = len(stream)
    
        # Call the binary mechanism function and store its list output in binary_results
        binary_results = binary_mechanism(T, epsilon, stream)
        
        # Add the results as a new column in the result DataFrame, named by the MunicipalityNo
        result_df[str(mun_no)] = binary_results

        i+=1

    end_time = time.time()

    # Print the time it took to run the mechanism loop
    duration = end_time - start_time
    print(f"The function took {duration} seconds to run.")

    # Upscale
    for col in result_df.columns[1:]:  # Skip the first column (HourDK)
        result_df[col] = upScale(result_df, col, thresh)

    # Save the result to a csv file
    result_df.to_csv("results/NumMun_noisy_result.csv", index=False)

    print("done")

# Main function that runs when the file is executed
if __name__ == "__main__":
    NumMun(1)