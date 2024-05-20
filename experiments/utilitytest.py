import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.scale import downScaleDf, upScaleDf, upScale, downScale
import math
from utils.clipData import clip_pr_column
from DifferentialApplication.NumMun import NumMun
from DifferentialApplication.Num import Num
from DifferentialApplication.Bin import Bin
from scipy.stats import gaussian_kde
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnb import NumMunUnb



def convert_df_to_numeric(df):
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    return df


np.random.seed(42) #random seed such that the tests generated are always the same

# # Load datasets

real_bin_df = pd.read_csv('results/Bin_result.csv')
real_num_fil_df  = pd.read_csv('results/num_fil_result.csv')
real_num_df = pd.read_csv('results/num_result.csv')
real_mun_df = pd.read_csv('results/real_consumption_sums.csv')
real_reg_df = pd.read_csv('results/regional_consumption_sums.csv')



# Parameters
delta = 0.001
B = 504
num_runs = 10
intermediate_steps = False
theta = 0.5


#epsilons = [0.1, 0.2, 0.5, 1, 1.5, 2]
#epsilons = [0.1, 0.5, 1, 2]
epsilons = [2, 1, 0.5, 0.1]

epsilon_errors = {epsilon: [] for epsilon in epsilons}

for epsilon in epsilons:

    print("\nrunning epsilon: ", epsilon)

    print("\nRunning Bin...")
    Bin(epsilon)
    print("\nRunning Mun...")
    Num(epsilon)
    print("\nRunning MunNum...")
    NumMun(epsilon)
    print("\nrunning NumMunUnb")
    NumMunUnb(epsilon)
    print("\nrunning NumMunUnbGeo")
    NumMunUnbGeo(epsilon)
    print("\nrunning NumMunUnbGeoLoc")
    NumMunUnbGeoLoc(epsilon)






    #update the dataframes
    Bin_df = pd.read_csv('results/Bin_noisy_result.csv')
    Num_fil_df = pd.read_csv('results/Num_fil_noisy_result.csv')
    Num_df = pd.read_csv('results/Num_noisy_result.csv')
    NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')
    NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
    NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
    NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')

    #Re initialize the dataframe paris
    dataframe_pairs = [
    ('Bin', Bin_df, real_bin_df),
    ('Num', Num_df, real_num_df),
    ('Num_fil', Num_fil_df, real_num_fil_df),
    ('NumMun', NumMun_df, real_mun_df),
    ('NumMunUnb', NumMunUnb_df, real_mun_df),
    ('NumMunUnbGeo', NumMunUnbGeo_df, real_reg_df),
    ('NumMunUnbGeoLoc', NumMunUnbGeoLoc_df, real_reg_df)
    ]


    for name, noisy_df, real_df in dataframe_pairs:
        if 'HourDK' in noisy_df.columns:
            noisy_df.drop(columns=['HourDK'], inplace=True)
        if 'HourDK' in real_df.columns:
            real_df.drop(columns=['HourDK'], inplace=True)

        # Convert columns to numeric
        noisy_df = noisy_df.apply(pd.to_numeric, errors='coerce')
        real_df = real_df.apply(pd.to_numeric, errors='coerce')

        # Calculate the absolute differences and find the maximum difference
        max_diff = real_df.diff().abs().max().max()
        
        if name != 'Bin': # dont scale down bin as it is already binary
            for column in noisy_df.columns:
                # Scale both dataframes by the maximum difference
                noisy_df[column] = noisy_df[column] / max_diff
                real_df[column] = real_df[column] / max_diff

        # To ensure changes are reflected outside the loop or in the original list, update the dataframes in the list:
        index = next(i for i, pair in enumerate(dataframe_pairs) if pair[0] == name)
        dataframe_pairs[index] = (name, noisy_df, real_df)




    outliers = {name: [] for name, _, __ in dataframe_pairs}
    errors = {name: [] for name, _, __ in dataframe_pairs}

    # Loop over each dataframe
    for name, noisy_df, real_df in dataframe_pairs:
        
        for muni in noisy_df.columns:
            
            for s, row in real_df.iterrows():  # t is the index, row is the row data
                if s == 0:
                    t = 1
                else:
                    t = s

              # muni is each column, makes sense for NumMun, but works for all dataframes
                real_value = row[muni]
                noisy_value = noisy_df.at[t, muni]
            

                # Check the specific dataframe and set the bound
                if name == 'Bin': #B = sqrt(T), so approx T^0.25 = 12 errors with 0.001 prob
                    bound = (1 / epsilon) * np.sqrt(((t+1) / B) + B) * np.log(1 / delta)
                elif name == 'NumMun':
                    T = len(noisy_df) # T = 1099 approx 1 errors
                    bound = (1 / epsilon) * np.log(T) * np.sqrt(np.log(t+1)) * np.log(1 / delta)
                elif name == 'Num' or name == "Num_fil":
                    T = len(noisy_df) #T=27048 approx 27 errrors
                    bound = (1 / epsilon) * np.log(T) * np.sqrt(np.log(t+1)) * np.log(1 / delta)
                else:
                    bound = ((1 / (theta * epsilon)) * ((np.log2(t + 1))**(1.5+theta)) * np.log2(1 / delta))

                # Outlier detection
                if not np.abs(real_value - noisy_value) <= bound:
                    outliers[name].append((muni, t))


                
                errors[name].append((real_value - noisy_value))

                    #print(f"\nmuni: {muni}, t: {t}, real_value: {real_value}, noisy_value: {noisy_value}, bound: {bound}")
                    #print(f"real-noisy difference: {np.abs(np.float64(real_value) - np.float64(noisy_value))}")


                
            

    # Aggregate results from this run
    for name in outliers:
        #average_outliers[name] += len(outliers[name])
        print("Outlier count: " , name, ": ", len(outliers[name]))

    

    epsilon_errors[epsilon] = errors
    #print("errors: ", errors)


    if intermediate_steps:
        # Print the count of outliers for each DataFrame
        for name, data in outliers.items():
            print(f"{name} - Total Outliers: {len(data)}")

       

# First, we'll collect data by name
name_data = {}
for epsilon, errors in epsilon_errors.items():
    for name, err in errors.items():
        if name not in name_data:
            name_data[name] = {}
        # Convert errors list to a numpy array for processing
        data = np.array(err)
        name_data[name][epsilon] = data

# Now, plot each name's data with all epsilons on the same plot
for name, datasets in name_data.items():
    plt.figure(figsize=(8, 4))
    for epsilon, data in datasets.items():
        # Generate a KDE for the error data
        density = gaussian_kde(data)

        # Set up the range for x values
        x = np.linspace(min(data), max(data), 100)
        y = density(x)

        # Plot each epsilon density
        plt.plot(x, y, label=f'Epsilon = {epsilon}')

    # Finalizing the plot
    plt.title(f'Error Density for {name} Across Epsilons')
    plt.xlabel('Error Value')
    plt.ylabel('Density')
    plt.legend()
    plt.grid(True)
    plt.show()