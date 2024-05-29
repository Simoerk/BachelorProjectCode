import pandas as pd
import numpy as np
from utils.scale import downScaleDf, upScaleDf, upScale, downScale
from utils.clipData import clip_pr_column
from DifferentialApplication.NumMun import NumMun
from DifferentialApplication.NumMunUnb import NumMunUnb
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
import math
from utils.laplace import *
from decimal import Decimal, getcontext
from utils.load_dataset import load_dataset
from utils.clipData import clip
import scipy.stats as stats

# Set the precision (number of decimal places)
getcontext().prec = 49

#random seed for testing
np.random.seed(42)

# Define a function to get the scale parameter as Decimal
def ai_decimal(i, epsilon):
    # Example conversion, replace with your actual scale logic
    return Decimal(ai(i, epsilon))

epsilons = [0.5, 5]
# Import and clip the real data
#real_df = pd.read_csv('results/real_consumption_sums.csv')
#real_df = clip_pr_column(real_df)



for epsilon in epsilons:
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
    #måske fjern
    unique_times = sorted(real_df['HourDK'].unique())
    real_df = real_df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')
    real_df = real_df.iloc[1:]
    real_df = real_df.cumsum()
    real_df.to_csv("results/real_consumption_sums_test.csv", index=False)
    #Make processed csv file
    #real_df = real_df.iloc[1:]
    #Make processed csv file MÅSKe fJERN?
    #real_df.insert(0, 'HourDK', unique_times[1:])

    



    # Load the noisy data
    #NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
    NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
    NumMunUnb_df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
    NumMun_df = pd.read_csv('results/NumMun_noisy_result.csv')


    #NumMunUnbGeoLoc_df = NumMunUnbGeoLoc_df.iloc[:, :-6]
    NumMunUnbGeo_df = NumMunUnbGeo_df.iloc[:, :-6]

    # List of dataframes for processing
    dfs = [NumMun_df, NumMunUnb_df, NumMunUnbGeo_df, real_df]
    #outliers = {name: [] for name in ['NumMun', 'NumMunUnb', 'NumMunUnbGeo', 'NumMunUnbGeoLoc', "real_df"]}
    outliers = {name: [] for name in ['NumMun_df', 'NumMunUnb_df', 'NumMunUnbGeo_df', "real_df"]}

    dfs = [df.drop(columns=['HourDK'], errors='ignore') for df in dfs]

    #print("NumMunUnbGeo_df max: ", NumMunUnbGeo_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max())
    #print("NumMunUnb_df max: ", NumMunUnb_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max())
    #print("NumMun_df max: ", NumMun_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max())
    #print("real max: ", real_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max())


    global_max = real_df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max()
    for df in dfs:
        for column in df.columns:
            df[column] = (df[column] - 0) / (global_max - 0)
        #print("max in ", ": ", df.apply(pd.to_numeric, errors='coerce').diff().abs().max().max())

    test = False


    for df_name, df in zip(outliers.keys(), dfs):
        if df_name == "real_df":
             continue
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0
        count6 = 0
        for muni in df.columns:
            for t, row in df.iterrows():  
                        if t == 0:
                            continue

                    
                        # Access values safely using .iloc to avoid index out of bounds
                        noisy_t = df[muni][t]
                        
                
                        real_t = dfs[3][int(muni)][t]
                        real_t_minus_1 = dfs[3][int(muni)][t-1]


                        #ai IS IMPOERNTANT
                        # Determine the number of bits needed for binary representation of t
                        num_bits = int(math.log2(t)) + 1
                        
                        # Convert t to binary form and pad with zeros
                        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
                        bin_t.reverse()
                        i = next(i for i, bit in enumerate(bin_t) if bit != 0)

                        T = len(df)
                        
                        
                        # noisy_t, real_t, real_t_minus_1 need to be Decimal
                        noisy_t_decimal = Decimal(str(noisy_t))
                        real_t_decimal = Decimal(str(real_t))
                        real_t_minus_1_decimal = Decimal(str(real_t_minus_1))

                        if df_name == "NumMun_df": #import scipy.stats.laplace.pdf(x, scale)
                            # Calculate probabilities using Decimal for high precision
                            #p_1 = (Decimal('1') / (Decimal('2') * Decimal('1')/epsilon)) * (np.exp(-abs(noisy_t_decimal - real_t_decimal) / (Decimal('1')/epsilon)))
                            #p_2 = (Decimal('1') / (Decimal('2') * Decimal('1')/epsilon)) * (np.exp(-abs(noisy_t_decimal - real_t_minus_1_decimal) / (Decimal('1')/epsilon)))

                            p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(np.log(T)/epsilon))
                            p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(np.log(T)/epsilon))

                            #print("p_1_old: ", p_1_old)
                            #print("p_2_old: ", p_2_old)
                            #print("p_1: ", p_1)
                            #print("p_2: ", p_2)

                        else: 
                            # Calculate probabilities using Decimal for high precision
                            #p_1_old = (Decimal('1') / (Decimal('2') * (ai_decimal(i, 0.5)/epsilon))) * (np.exp(-abs(noisy_t_decimal - real_t_decimal) / (ai_decimal(i, 0.5)/epsilon)))
                            #p_2_old = (Decimal('1') / (Decimal('2') * (ai_decimal(i, 0.5)/epsilon))) * (np.exp(-abs(noisy_t_decimal - real_t_minus_1_decimal) / (ai_decimal(i, 0.5)/epsilon)))
                            
                            p_1 = stats.laplace.pdf(noisy_t - real_t, scale=(ai(i, 0.5)/np.float64(epsilon)))
                            p_2 = stats.laplace.pdf(noisy_t - real_t_minus_1, scale=(ai(i, 0.5)/np.float64(epsilon)))

                        # Compute the ratio of probabilities and compare it to exp(1)
                        if p_2 == 0:  # Avoid division by zero
                            ratio = Decimal('Infinity')  # ratio to infinity if p_2 is zero because large
                        if p_1 == 0:
                            print("Error: p_1 is zero")
                            continue
                        else:
                            ratio = p_1 / p_2

                        exp_epsilon = np.exp(epsilon)
                        
                        if epsilon == 0.5 and ratio < exp_epsilon:
                            if ratio > (exp_epsilon-0.01):
                                print("epsilon : ", epsilon)
                                print("epsilon.exp(): ", epsilon.exp())
                                print("ratio: ", ratio)
                                print("p_1: ", p_1)
                                print("p_2: ", p_2)
                        if epsilon == 5 and ratio < exp_epsilon:
                            if ratio > (exp_epsilon-50):
                                print("epsilon : ", epsilon)
                                print("epsilon.exp(): ", epsilon.exp())
                                print("ratio: ", ratio)
                                print("p_1: ", p_1)
                                print("p_2: ", p_2)
                                
                        
                                
                      

                        

