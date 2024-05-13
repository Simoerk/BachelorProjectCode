import pandas as pd
import numpy as np
from utils.scale import downScaleDf, upScaleDf, upScale, downScale


real_df = pd.read_csv('results/real_consumption_sums.csv')
NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')


NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, :-6]
NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]


# List of dataframes for processing
dfs = [NumMun_df, NumMunUnb_df, NumMunUnbGeo_df, NumMunUnbGeoLoc_df, real_df]
#outliers = {name: [] for name in ['NumMun', 'NumMunUnb', 'NumMunUnbGeo', 'NumMunUnbGeoLoc', "real_df"]}
outliers = {name: [] for name in ['NumMun_df', 'NumMunUnb_df', 'NumMunUnbGeo_df', 'NumMunUnbGeoLoc_df', "real_df"]}

dfs = [df.drop(columns=['HourDK']) for df in dfs]


global_max = real_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max()
for df in dfs:
    for column in df.columns:
        df[column] = (df[column] - 0) / (global_max - 0)



exp = np.exp(1)
for df_name, df in zip(outliers.keys(), dfs):
    for t, row in df.iterrows():  # Start from 1 because we need t-1
            for muni in df.columns:
                # Access values safely using .iloc to avoid index out of bounds
                noisy_t = df.iloc[t][muni]
                
                real_t = dfs[4].iloc[t][muni]
                real_t_minus_1 = dfs[4].iloc[t-1][muni]
                
                # Calculate probabilities assuming your noise model is correctly specified
                p_1 = 0.5 * np.exp(-(np.float64(noisy_t) - np.float64(real_t)))
                p_2 = 0.5 * np.exp(-(np.float64(noisy_t) - np.float64(real_t_minus_1)))
                
                # Compute the ratio of probabilities and compare it to exp(1)
                if p_2 == 0:  # Avoid division by zero
                    ratio = np.inf  # Set ratio to infinity if p_2 is zero
                else:
                    ratio = p_1 / p_2

                if ratio > exp: 
                    print(f"Ratio condition met for {muni} at time {t} in {df_name} with ratioe: ", ratio, ">", np.exp(1))
                    print("np.float64(noisy_t): ", np.float64(noisy_t))
                    print("np.float64(real_t)", np.float64(real_t))
                    print("np.float64(real_t_minus_1)", np.float64(real_t_minus_1))
                    outliers[df_name].append((t, muni, ratio))
                else:
                    #print("all good: ", t)
                    print("ratio: ", ratio, "<=", exp)
                    print("p1: ", p_1, " p_2: ", p_2)
    print("df: ", df_name)
                

# Print the count of outliers for each DataFrame
for name, data in outliers.items():
    print(f"{name} - Total Outliers: {len(data)}")
