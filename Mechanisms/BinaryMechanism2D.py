import numpy as np
import pandas as pd
import math
from utils.laplace import *
from utils.muniRegion import *
import sys
import warnings

# Removing warning from a future version of python
warnings.filterwarnings('ignore', category=FutureWarning, message=".*Series.__getitem__ treating keys as positions is deprecated.*")


# Function that implements a geographical unbounded binary mechanism 
def binary_mechanism_geo(epsilon, df, result_df, theta):

    print("begin binary mechanism unbounded geo")

    # Get the region dictionary
    region_dict = give_regionDictionary()
    # Create a list of regions and add 'DK' for the total of all regions
    regions = list(region_dict.keys()) + ['DK']
    # Create an empty DataFrame with these regions as columns
    regional_data_df = pd.DataFrame(columns=regions)

    num_rows, num_cols = df.shape

    n = len(give_muni())  # Number of municipalities
    alpha2D = [[] for _ in range(n)] # 2D list to store alpha_i values across time and geography
    alpha_hat2D = [[] for _ in range(n)]

    problem_list =[]

    t_last =  1

    # Loop through each time step
    for t in range(t_last, t_last+num_rows):

        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]

        # Find the least significant non-zero bit in binary representation of t
        bin_t.reverse() # bin_t was in reverse order
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        k = 0
        
        regional_values, regional_tresh = initialize_region_dictionaries()

        # Loops through each municipality
        for muni_number in give_region():
            # Check if the municipality number exists as a column in the DataFrame
            muni_number = int(muni_number)
            if muni_number in df.columns:

                if muni_number not in result_df.columns:
                    result_df[muni_number] = None
            
                # Extend alpha lists
                for alpha in alpha2D:
                    if len(alpha) < num_bits:
                        alpha.extend([0])
                for alpha_hat in alpha_hat2D:
                    if len(alpha_hat) < num_bits:
                        alpha_hat.extend([0])
                
                # Update alpha_i
                alpha2D[k][i] = (sum(alpha2D[k][j] for j in range(i)) + df[muni_number][t-1])

                if math.isnan(alpha2D[k][i]):
                    if muni_number not in problem_list:
                        problem_list.append(muni_number)

                # Add the value to the regional sum
                regional_values[give_region().get(str(muni_number))] += (sum(alpha2D[k][j] for j, bit in enumerate(bin_t) if bit == 1))
                
                # Set unused alpha values to 0
                for j in range(i):
                    alpha2D[k][j] = 0
                    alpha_hat2D[k][j] = 0

                # Add Laplacian noise to alpha_hat_i usind the ai function in laplace
                alpha_hat2D[k][i] = laplace_mechanism(alpha2D[k][i], ai(i, theta),epsilon)
                result_df.loc[t-1, muni_number] = (sum(alpha_hat2D[k][j] for j, bit in enumerate(bin_t) if bit == 1))
                k+=1

            else:
                print("ERROR :", muni_number)
                sys.exit()
                
        # Calculating the total sum of all regions and get the DK value
        DK = 0.0
        for region in regional_values:    
            DK += regional_values[region]
            regional_data_df.at[t-1, region] = laplace_mechanism(regional_values[region],ai(i, theta),epsilon)
 
        # Add noise to DK value
        regional_data_df.at[t-1, "DK"] = laplace_mechanism(DK, ai(i, theta),epsilon)

    # Concatenate the result DataFrame with the regional data DataFrame and return the result
    result_df_con = pd.concat([result_df, regional_data_df], axis=1)
    return result_df_con

