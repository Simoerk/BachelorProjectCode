import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
from utils.muniRegion import *

data = pd.read_csv("data/Municipality.csv")
muni = data['number'].to_numpy()




# Define the ai function based on Corollary 4.4
def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)



def append_columns_individual(df, row_index, values_list, DK_alpha_hat):
    # Navnene på de forskellige regioner
    regions = ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland", "DK"]
    
    # Tilføj hver værdi individuelt til den tilsvarende kolonne
    for idx, value in enumerate(values_list):
        df.loc[row_index, regions[idx]] = value
    
    # Tilføj DK_alpha_hat til kolonnen "DK"
    df.loc[row_index, "DK"] = DK_alpha_hat



# Define the modified binary mechanism as an unbounded function
def binary_mechanism_unbounded(epsilon, df, result_df, t_last, theta=1):

    print("begin binary mechanism unbounded")

    df = df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')

    num_rows, num_cols = df.shape

    alpha2D = []
    alpha_hat2D = []
   
    i_list = [0] + count_regions()


 
    #print("df columns:", df.columns)

    for t in range(t_last, t_last+num_rows):

        kommunal_vars_alpha = []
        DK_alpha_hat = 0

        #print("t = ", t)
        # Determine the number of bits needed for binary representation of t
        num_bits = int(math.log2(t)) + 1
        
        # Convert t to binary form and pad with zeros
        bin_t = [int(x) for x in bin(t)[2:].zfill(num_bits)]
        bin_t.reverse()
        i = next(i for i, bit in enumerate(bin_t) if bit != 0)
        k = 0
        b = 1


        for muni_number in give_region():
            # Check if the municipality number exists as a column in the DataFrame
            muni_number = int(muni_number)

            if muni_number in df.columns:
                

                alpha2D.append([])
                alpha_hat2D.append([])
                
                # Can be optimized with a counterthing
                for alpha in alpha2D:
                    if len(alpha) < num_bits:
                        alpha.extend([0])
                for alpha_hat in alpha_hat2D:
                    if len(alpha_hat) < num_bits:
                        alpha_hat.extend([0])


                # Update alpha_i
                alpha2D[k][i] = (sum(alpha2D[k][j] for j in range(i)) + df[muni_number][t-1])

                # Reset previous values to 0
                for j in range(i):
                    alpha2D[k][j] = 0
                    alpha_hat2D[k][j] = 0

                # Add Laplacian noise to alpha_hat_i
            
                alpha_hat2D[k][i] = alpha2D[k][i] + laplace_mechanism(ai(i, theta)/epsilon)
                
                # append
                
                result_df.loc[t, muni_number] = (sum(alpha_hat2D[k][i] for j, bit in enumerate(bin_t) if bit == 1))

                #print("sum: ", (sum(alpha_hat[k][i] for j, bit in enumerate(bin_t) if bit == 1)))

                
                region_alpha = 0
                if k == i_list[b]:
                    #print("k:", k)
                    #print("i_list: ", i_list[b])
                    ith_elements = [sublist[i] for sublist in alpha2D[i_list[b-1]:i_list[b]]]
                    region_alpha = sum(ith_elements)
                    #print("region alpha: ",region_alpha)
                    #print("i: ", i)
                    region_alpha_hat = region_alpha + laplace_mechanism(ai(i, theta)/epsilon)
                    b+=1
                    kommunal_vars_alpha.append(region_alpha_hat)
                

                k+=1
            else:
                print(muni_number)
               
        

        ith_elements = [sublist[i] for sublist in alpha2D if len(sublist) > i]
        DK_alpha_hat = sum(ith_elements)
        DK_alpha_hat += laplace_mechanism(ai(i, theta)/epsilon)


        #print("len: ", len(kommunal_vars_alpha))


        append_columns_individual(result_df, i, kommunal_vars_alpha, DK_alpha_hat)


    
        


    print("result df: ", result_df)

    return result_df

