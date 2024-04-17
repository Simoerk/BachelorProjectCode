import numpy as np
import pandas as pd
import math
from utils.laplace import *
from utils.muniRegion import *
import sys

data = pd.read_csv("data/Municipality.csv")
muni = data['number'].to_numpy()




# Define the ai function based on Corollary 4.4
def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)




# Define the modified binary mechanism as an unbounded function
def binary_mechanism_unbounded(epsilon, df, result_df, t_last, theta, unique_times):

    print("begin binary mechanism unbounded")


    regional_data_df = pd.DataFrame(columns=["Hovedstaden", "Sjaelland", "Syddanmark", "Midtjylland", "Nordjylland", "DK"])


    df = df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    #This is to make a csv file
    df = df.iloc[1:]
    df.insert(0, 'HourDK', unique_times[1:])
    df.to_csv("results/processed_data.csv", index=False)
    df = df.drop('HourDK', axis=1)



    num_rows, num_cols = df.shape

    n = len(give_muni())  # Number of municipalities
    alpha2D = [[] for _ in range(n)]
    alpha_hat2D = [[] for _ in range(n)]



    problem_list =[]




    for t in range(t_last, t_last+num_rows):

        print("time: ", t-1)

        
        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        k = 0
        
        regional_values = {
        "Hovedstaden": 0.0,
        "Sjaelland": 0.0,
        "Syddanmark": 0.0,
        "Midtjylland": 0.0,
        "Nordjylland": 0.0
        }

       


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

                regional_values[give_region().get(str(muni_number))] += (sum(alpha2D[k][j] for j, bit in enumerate(bin_t) if bit == 1))


                # Reset previous values to 0
                for j in range(i):
                    alpha2D[k][j] = 0
                    alpha_hat2D[k][j] = 0

                # Add Laplacian noise to alpha_hat_i
            
                alpha_hat2D[k][i] = alpha2D[k][i] + laplace_mechanism(ai(i, theta)/epsilon)

            


                result_df.loc[t-1, muni_number] = (sum(alpha_hat2D[k][j] for j, bit in enumerate(bin_t) if bit == 1))

           

                k+=1

            else:
                print("ERROR :", muni_number)
                sys.exit()
                
               
        


        DK = 0.0
        for region in regional_values:
            regional_data_df.at[t-1, region] = regional_values[region] + laplace_mechanism_sensitivity(ai(i, theta)/epsilon, count_municipalities_in_region(region))
            DK += regional_values[region] 

        regional_data_df.at[t-1, "DK"] = DK + laplace_mechanism_sensitivity(ai(i, theta)/epsilon, len(give_region()))




    result_df_con = pd.concat([result_df, regional_data_df], axis=1)

    




    return result_df_con

