import pandas as pd
from Mechanisms.BinaryMechanism2DLocal import binary_mechanism_geo_local
from utils.clipData import *
from utils.scaleData import downScaleDf
from utils.scaleData import upScaleDf
from utils.loadDataset import load_dataset
import time

# NumMunUnbGeo(epsilon) applies the binary mechanism to the electricity dataset from Energinet
def NumMunUnbGeoLoc(epsilon):

    # To preserve epsilon differential privacy because two epsilon differential privacy mechanisms are called
    epsilonMech = epsilon * 0.9
    epsilonClip = epsilon * 0.1

    # Load dataset with Municipality, time and housing/heating category
    df_mun = load_dataset("data/muni_data.csv", 1000000)

    # Group by HourDK and MunicipalityNo and sum the ConsumptionkWh, removing categories
    df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')

    # Create the result df
    result_df = pd.DataFrame()
    unique_times = sorted(df_mun['HourDK'].unique())
    result_df['HourDK'] = unique_times[1:]

    # Pivot to make so that municipalities represent the columns
    df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    # Remove first row to account for uneven time intervals in the dataset
    df = df.iloc[1:]

    # Clip the data
    df, _ = clip_pr_column(df, epsilonClip)

    # Downscale
    df, thresh_df = downScaleDf(df)

    # Calling the local unbounded geographical binary mechanism with timer
    start_time = time.time()
    result_df, thresh_df = binary_mechanism_geo_local(epsilonMech, df, result_df, 0.5, thresh_df)
    end_time = time.time()

    # Print the time it took to run
    duration = end_time - start_time
    print(f"The function took {duration} seconds to run.")

    # Upscale
    result_df = upScaleDf(result_df, thresh_df)

    # Save to csv file
    result_df.to_csv("results/NumMunUnbGeoLoc_noisy_result.csv", index=False)
    thresh_df.to_csv("results/NumMunUnbGeoLoc_noisy_thresh.csv", index=False)
    print("done")

# Main function that runs when the file is executed
if __name__ == "__main__":
    NumMunUnbGeoLoc(1)


