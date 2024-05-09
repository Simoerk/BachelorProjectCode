import numpy as np
import pandas as pd
import math
from utils.laplace import *
from utils.muniRegion import *
import sys
import warnings


warnings.filterwarnings('ignore', category=FutureWarning, message=".*Series.__getitem__ treating keys as positions is deprecated.*")



# Define the modified binary mechanism as an unbounded function
def binary_mechanism_unbounded_local(epsilon, df, result_df, theta, scale_df):

    print("begin binary mechanism unbounded")

    # Get the region dictionary
    region_dict = give_regionDictionary()
    # Create a list of regions and add 'DK' for the total of all regions
    regions = list(region_dict.keys()) + ['DK']
    # Create an empty DataFrame with these regions as columns
    regional_data_df = pd.DataFrame(columns=regions)

    num_rows, num_cols = df.shape

    n = len(give_muni())  # Number of municipalities
    alpha2D = [[] for _ in range(n)]
    alpha_hat2D = [[] for _ in range(n)]

    problem_list =[]


    # Call the function to create the dictionaries
    regional_values, regional_tresh = initialize_region_dictionaries()


    #Find scales for regions
    max_region_thresh = 0.0
    # Create an empty DataFrame with these regions as columns
    regional_scale_df = pd.DataFrame(columns=regions)
    pd.concat([scale_df, regional_scale_df], axis=1)
    scale_df = scale_df.copy()

    # Update regional thresholds based on the maximum values from `scale_df`
    for muni_number in give_region():
        muni_number = int(muni_number)
        region_key = give_region().get(str(muni_number))  # Get the region name from muni_number
        current_thresh = regional_tresh.get(region_key, 0)  # Use existing or default to 0
        scale_val = scale_df.loc['max_val', muni_number] if 'max_val' in scale_df.index else 0
        regional_tresh[region_key] = max(scale_val, current_thresh)

    # Update the scale_df DataFrame with new max values for each region
    for region, thresh in regional_tresh.items():
        scale_df.loc['max_val', region] = thresh  # This directly sets the value in the DataFrame
        max_region_thresh = max(max_region_thresh, thresh)  # Calculate the maximum for 'DK'

    # Set the DK value
    scale_df.loc['max_val', 'DK'] = max_region_thresh

    # Optionally, to reduce fragmentation, reassign a copy to itself
    scale_df = scale_df.copy()

    #print("Updated scale_df: ", scale_df)

    t_last = 1

    for t in range(t_last, t_last+num_rows):

        #print("time: ", t-1)

        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        k = 0
        
        for region in regional_values:
            regional_values[region] = 0.0
        

        for muni_number in give_region():
            # Check if the municipality number exists as a column in the DataFrame
            muni_number = int(muni_number)

            if muni_number in df.columns:


                if muni_number not in result_df.columns:
                    result_df[muni_number] = None
            
            
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

                regional_values[give_region().get(str(muni_number))] += (sum(alpha2D[k][j] for j, bit in enumerate(bin_t) if bit == 1)) * scale_df.loc['max_val', muni_number]
            
                # Reset previous values to 0
                for j in range(i):
                    alpha2D[k][j] = 0
                    alpha_hat2D[k][j] = 0

                # Add Laplacian noise to alpha_hat_i
                #lap = laplace_mechanism(ai(i, theta),epsilon)
                #lap = laplace_mechanism(epsilon)
                alpha_hat2D[k][i] = laplace_mechanism(alpha2D[k][i], ai(i, theta),epsilon)
                result_df.loc[t-1, muni_number] = (sum(alpha_hat2D[k][j] for j, bit in enumerate(bin_t) if bit == 1))
                k+=1

            else:
                print("ERROR :", muni_number)
                sys.exit()
                

        DK = 0.0
        for region in regional_values:
            DK += regional_values[region]
            #regional_data_df.at[t-1, region] = (regional_values[region]/regional_tresh[region]) + laplace_mechanism(epsilon)
            regional_data_df.at[t-1, region] = laplace_mechanism((regional_values[region]/regional_tresh[region]),ai(i, theta),epsilon)
            
        regional_data_df.at[t-1, "DK"] = laplace_mechanism((DK/max_region_thresh),ai(i, theta),epsilon)
        #regional_data_df.at[t-1, "DK"] = (DK/max_region_thresh + laplace_mechanism(epsilon))

    result_df_con = pd.concat([result_df, regional_data_df], axis=1)
    return result_df_con, scale_df

