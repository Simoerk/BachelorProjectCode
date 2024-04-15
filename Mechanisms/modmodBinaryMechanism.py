import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
from utils.muniRegion import *
import sys

data = pd.read_csv("data/Municipality.csv")
muni = data['number'].to_numpy()




# Define the ai function based on Corollary 4.4
def ai(i, theta):
    # Implementing ai as per Corollary 4.4
    return (i + 1)**(1 + theta)



def insert_kommunal_values(df, row_index, kommunal_vars, DK_alpha_hat):
    # Column names corresponding to the regions, excluding 'DK' since it's handled separately
    regions = ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland"]
    
    # Insert each kommunal variable into the corresponding column
    for idx, value in enumerate(kommunal_vars):
        df.at[row_index, regions[idx]] = value
    
    # Insert DK_alpha_hat into the column "DK"
    df.at[row_index, "DK"] = DK_alpha_hat





# Define the modified binary mechanism as an unbounded function
def binary_mechanism_unbounded(epsilon, df, result_df, t_last, theta=1):

    print("begin binary mechanism unbounded")

    # List of new columns to add
    regions = ["Hovedstaden", "Sjælland", "Syddanmark", "Midtjylland", "Nordjylland", "DK"]
    regional_data_df = pd.DataFrame()
    for region in regions:
        regional_data_df[region] = None 

    df = df.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')


    num_rows, num_cols = df.shape

    n = len(give_muni())  # Number of municipalities
    alpha2D = [[] for _ in range(n)]
    alpha_hat2D = [[] for _ in range(n)]

    i_list = [0] + count_regions()


    i_list_sum = []
    current_sum = 0
    for num in i_list:
        current_sum += num
        i_list_sum.append(current_sum)

    problem_list =[]



 
    #print("df columns:", df.columns)

    for t in range(t_last, t_last+num_rows):

        print("time: ", t)

        
        DK_alpha_hat = 0
        kommunal_vars_alpha = np.zeros(5)

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


                if muni_number not in result_df.columns:
                    result_df[muni_number] = None
            
                #print("alpha2D: ", alpha2D)
                #print("alpha2D_hat: ", alpha_hat2D)
                
                # Can be optimized with a counterthing
                for alpha in alpha2D:
                    if len(alpha) < num_bits:
                        alpha.extend([0])
                        #print("len(alpha): ", len(alpha))
                        #print("num_bits: ", num_bits)
                        #print("exstended alpa")
                for alpha_hat in alpha_hat2D:
                    if len(alpha_hat) < num_bits:
                        alpha_hat.extend([0])
                        #print("len(alpha): ", len(alpha))
                        #print("num_bits: ", num_bits)
                        #print("exstended alpahat")

                


                # Update alpha_i
                alpha2D[k][i] = (sum(alpha2D[k][j] for j in range(i+1)) + df[muni_number][t-1])

                if math.isnan(alpha2D[k][i]) and k==-19:

                    print("muni: ", muni_number)
                    print("k: ", k)

                    print("df[muni_number][t-1]: ", df[muni_number][t-1])
                    print("alpha2D[k][i]", alpha2D[k][i])
                    print("len alpha2D[k]: ", len(alpha2D[k]))
                    print("alpha2D[k]: ", alpha2D[k], "\n")
                    #print("alpaha2d: ", alpha2D)

                    if muni_number not in problem_list:
                        problem_list.append(muni_number)


                # Reset previous values to 0
                for j in range(i):
                    alpha2D[k][j] = 0
                    alpha_hat2D[k][j] = 0

                # Add Laplacian noise to alpha_hat_i
            
                alpha_hat2D[k][i] = alpha2D[k][i] + laplace_mechanism(ai(i, theta)/epsilon)
                #print("alpha_hat2D[k][i]: ", alpha_hat2D[k][i], "\n")
                
                
                # append
                
                result_df.loc[t, muni_number] = (sum(alpha_hat2D[k][i] for j, bit in enumerate(bin_t) if bit == 1))

                #print("sum: ", (sum(alpha_hat[k][i] for j, bit in enumerate(bin_t) if bit == 1)))

                

                # RETHINK!
                if k == i_list_sum[b]:
                    #print("k: ", k)
                    #print("i_list: ", i_list[b])
                    region_alpha = 0
                    #print("i: ", i)
                    ith_elements = [sublist[i] for sublist in alpha2D[i_list_sum[b-1]:i_list_sum[b]]]

                    #print("alpha2D[i_list[b-1]:i_list[b]-1] :", alpha2D[i_list_sum[b-1]:i_list_sum[b]])
                    #print("alpha2D[i_list[b-1]: ", alpha2D[i_list_sum[b-1]])
                    #print("alpha2D[i_list[b]]: ", alpha2D[i_list_sum[b]])
                    #print("ith_elements in k=: ", ith_elements)
                    region_alpha = sum(ith_elements)
                    #print("region_alpha: ", region_alpha)
                    #print("region alpha: ",region_alpha)
                    #print("i: ", i)
                    region_alpha_hat = region_alpha + laplace_mechanism(ai(i, theta)/epsilon)
                    b+=1
                    kommunal_vars_alpha.append(region_alpha_hat)
                k+=1
            else:
                print("ERROR :", muni_number)
                sys.exit()
                
               
        




        ith_elements = [sublist[i] for sublist in alpha2D]
        #print("ith_elements outside: ", ith_elements)
        DK_alpha_hat = sum(ith_elements)
        DK_alpha_hat += laplace_mechanism(ai(i, theta)/epsilon)

        #print("Komvars: ",kommunal_vars_alpha)
        #print("dk_alpha: ", DK_alpha_hat)


        #print("len: ", len(kommunal_vars_alpha))


        insert_kommunal_values(regional_data_df, t, kommunal_vars_alpha, DK_alpha_hat)
        #print(regional_data_df.iloc[t])

    
        



    result_df_con = pd.concat([result_df, regional_data_df], axis=1)

    print("\n")
    print("regional data df")
    print(regional_data_df)
    print(regional_data_df.shape)

    print("result_df_con")
    print(result_df_con.shape)


    print("result_df")
    print(result_df.shape)
    #print("problist: ", problem_list)

    print("\n")

    return result_df_con

