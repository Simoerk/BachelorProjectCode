import pandas as pd
import numpy as np
from DifferentialApplication.Num import Num
from DifferentialApplication.Bin import Bin
from decimal import Decimal, getcontext
import scipy.stats as stats


# Experiment to find if any indexes immidiately next to eachother 
# within the same are differentially private.
# Only for applications without any geographical information

# Set the precision (number of decimal places)
getcontext().prec = 49

# Random seed for testing
np.random.seed(42)

epsilons = [0.1, 0.5, 1, 2]

for epsilon in epsilons:
    print("Epsilon: ", epsilon)

    Bin(epsilon)
    Num(epsilon)

    # Load datasets
    real_bin_df = pd.read_csv('results/Bin_result.csv')
    real_num_fil_df  = pd.read_csv('results/num_fil_result.csv')
    real_num_df = pd.read_csv('results/num_result.csv')
    Bin_df = pd.read_csv('results/Bin_noisy_result.csv')
    Num_fil_df = pd.read_csv('results/Num_fil_noisy_result.csv')
    Num_df = pd.read_csv('results/Num_noisy_result.csv')

    # Pairing noisy and real dataframes
    dataframe_pairs = [
        ('Bin', Bin_df, real_bin_df),
        ('Num', Num_df, real_num_df),
        ('Num_fil', Num_fil_df, real_num_fil_df),
    ]

    # Calculate the length of the dataframes
    T = len(real_num_df)
    T_fil = len(real_num_fil_df)

    print("Scaling...")
    for name, noisy_df, real_df in dataframe_pairs:
        if 'HourDK' in real_df.columns:
            noisy_df.drop(columns=['HourDK'], inplace=True)
            real_df.drop(columns=['HourDK'], inplace=True)

        # Convert columns to numeric
        noisy_df = noisy_df.apply(pd.to_numeric, errors='coerce')
        real_df = real_df.apply(pd.to_numeric, errors='coerce')

        # Calculate the absolute differences and find the maximum difference
        max_diff = real_df.diff().abs().max().max()
        
        for column in real_df.columns:
            # Scale both dataframes by the maximum difference
            noisy_df[column] = noisy_df[column] / max_diff
            real_df[column] = real_df[column] / max_diff

        # To ensure changes are reflected outside the loop or in the original list
        # and update the dataframes in the list:
        index = next(i for i, pair in enumerate(dataframe_pairs) if pair[0] == name)
        dataframe_pairs[index] = (name, noisy_df, real_df)

    print("Done scaling...")


    outliers = {name: [] for name, _, __ in dataframe_pairs}

    print("running check...")
    # Loop over each dataframe
    for name, noisy_df, real_df in dataframe_pairs:
        for muni in real_df.columns: 
            for s, row in real_df.iterrows():  # t is the index, row is the row data
                if s == 0:
                    t = 1
                else:
                    t = s

                # muni is each column, makes sense for NumMun, but works for all dataframes
                # Access values safely using .iloc to avoid index out of bounds
                noisy_t = noisy_df[muni][t]
                
                real_t = real_df[muni][t]
                real_t_minus_1 = real_df[muni][t-1]
                
                # noisy_t, real_t, real_t_minus_1 need to be Decimal
                noisy_t_decimal = Decimal(str(noisy_t))
                real_t_decimal = Decimal(str(real_t))
                real_t_minus_1_decimal = Decimal(str(real_t_minus_1))

                if name == "Bin":
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(1/epsilon))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(1/epsilon))
                elif name == "Num":
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(1/(epsilon/np.log(T))))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(1/(epsilon/np.log(T))))
                else:
                    p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(1/(epsilon/np.log(T_fil))))
                    p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(1/(epsilon/np.log(T_fil))))
                
                if p_2 == 0:  # Avoid division by zero
                    ratio = np.inf  # Set ratio to infinity if p_2 is zero
                else:
                    ratio = p_1 / p_2
                
                exp_epsilon = np.exp(epsilon)
                exp_epsilon_2 = np.exp(2*epsilon)

                if ratio > exp_epsilon and name != "Bin":  
                    outliers[name].append((t, muni, ratio))

                elif ratio > exp_epsilon_2 and name == "Bin":
                    outliers[name].append((t, muni, ratio))

    print("Done running check...")

    # Print the count of outliers for each DataFrame
    for name, data in outliers.items():
        print(f"{name} - Total Outliers: {len(data)}")




