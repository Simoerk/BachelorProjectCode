import pandas as pd
from Mechanisms.BinaryMechanism2D import binary_mechanism_geo
from utils.clipData import clip
from utils.loadDataset import load_dataset
from utils.scaleData import downScale, upScale
import time

# NumMunUnbGeo(epsilon) applies the binary mechanism to the electricity dataset from Energinet
def NumMunUnbGeo(epsilon):

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

    # Create result dataframe
    result_df = pd.DataFrame()
    unique_times = sorted(df_mun['HourDK'].unique())
    result_df['HourDK'] = unique_times[1:]

    # Pivot such that the columns represent the municipalities
    df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    # Remove first row to account for uneven time intervals in the dataset. 
    # Should be done before clipping and scaling for correctness, but this causes some smaller problems when clipping.
    df = df.iloc[1:]

    # Calling the unbounded geographical binary mechanism with timer
    start_time = time.time()
    result_df = binary_mechanism_geo(epsilon, df, result_df, 0.5)
    end_time = time.time()

    # Print the time
    duration = end_time - start_time
    print(f"The function took {duration} seconds to run.")

    # Upscale
    for col in result_df.columns[1:]:  # Skip the first column (HourDK)
        result_df[col] = upScale(result_df, col, thresh)

    # Save to dataframe
    result_df.to_csv("results/NumMunUnbGeo_noisy_result.csv", index=False)
    print("done")

# Main function that runs when the file is executed 
if __name__ == "__main__":  
    NumMunUnbGeo(1)