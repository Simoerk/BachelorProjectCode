import pandas as pd
import numpy as np
from DifferentialApplication.NumMun import NumMun
from DifferentialApplication.NumMunUnb import NumMunUnb
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
import scipy.stats as stats
import math
from utils.laplace import *
from decimal import Decimal, getcontext
from utils.loadDataset import load_dataset
from utils.clipData import clip

# Experiment to find if any indexes immidiately next to eachother 
# within the same  municipalities are differentially private

# Set the precision (number of decimal places)
getcontext().prec = 49

#random seed for testing
np.random.seed(42)

epsilons = [0.1, 1, 2]

for epsilon in epsilons:
    print("\n")
    print("Epsilon: ", epsilon)

    # Run the differential privacy applications
    np.random.seed(42)
    NumMun(np.float64(epsilon))
    np.random.seed(42)
    NumMunUnb(np.float64(epsilon))
    np.random.seed(42)
    NumMunUnbGeo(np.float64(epsilon))
    np.random.seed(42)
    real_df = load_dataset("data/muni_data.csv", 1000000)
    real_df['ConsumptionkWh'], thresh = clip(real_df, 'ConsumptionkWh', np.float64(epsilon))
    
    # Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
    real_df = real_df.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')
    unique_times = sorted(real_df['HourDK'].unique())
    real_df = real_df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    real_df = real_df.iloc[1:]
    real_df = real_df.cumsum()

    # Load the noisy data
    NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
    NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
    NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')

    NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]

    # List of dataframes for processing
    dfs = [NumMun_df, NumMunUnb_df, NumMunUnbGeo_df, real_df]
    outliers = {name: [] for name in ['NumMun_df', 'NumMunUnb_df', 'NumMunUnbGeo_df', "real_df"]}

    dfs = [df.drop(columns=['HourDK'], errors='ignore') for df in dfs]

    global_max = real_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max()
    for df in dfs:
        for column in df.columns:
            df[column] = (df[column] - 0) / (global_max - 0)

    test = False

    for df_name, df in zip(outliers.keys(), dfs):
        if df_name == "real_df":
             continue
        for muni in df.columns:
            for t, row in df.iterrows():  
                if t == 0:
                    continue

            
                # Access values safely using .iloc to avoid index out of bounds
                noisy_t = df[muni][t]
                
        
                real_t = dfs[3][int(muni)][t]
                real_t_minus_1 = dfs[3][int(muni)][t-1]

                # Determine the number of bits needed for binary representation of t
                num_bits = int(math.log2(t)) + 1
                
                # Convert t to binary form and pad with zeros
                bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
                bin_t.reverse()
                i = next(i for i, bit in enumerate(bin_t) if bit != 0)
                
                noisy_t_decimal = Decimal(str(noisy_t))
                real_t_decimal = Decimal(str(real_t))
                real_t_minus_1_decimal = Decimal(str(real_t_minus_1))

                T = len(df)

                if df_name == "NumMun_df": 
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(np.log(T)/epsilon))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(np.log(T)/epsilon))
                
                if df_name == "NumMunUnb_df": 
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(np.log(T)/epsilon))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(np.log(T)/epsilon))

                else: 
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=((ai(i, 0.5)*3)/np.float64(epsilon)))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=((ai(i, 0.5)*3)/np.float64(epsilon)))

                # Compute the ratio of probabilities and compare it to exp(1)
                if p_2 == 0:  # Avoid division by zero
                    ratio = np.inf()
                if p_1 == 0:
                    ratio = np.inf()
                    continue
                else:
                    ratio = p_1 / p_2

                exp_epsilon = np.exp(epsilon)


                if ratio > exp_epsilon: 
                    print(f"Ratio larger than allowed for {muni} at time {t+1} in {df_name} with ratioe: ", ratio, ">", exp_epsilon)
                    outliers[df_name].append((t, muni, ratio))


    # Print the count of outliers for each DataFrame
    for name, data in outliers.items():
        print(f"Epsilon: {epsilon} Application: {name} - Total Outliers: {len(data)}")

    