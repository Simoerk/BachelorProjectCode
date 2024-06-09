import pandas as pd
import matplotlib.pyplot as plt
from DifferentialApplication.NumMunUnbGeoLoc import NumMunUnbGeoLoc
from DifferentialApplication.NumMunUnbGeo import NumMunUnbGeo
from DifferentialApplication.NumMunUnb import NumMunUnb
from DifferentialApplication.NumMun import NumMun
from experiments.compareApplications import show_comparison_for_specific_muni

# This experiment has two main functions:
# compare_epsilons_across_applications() which to a single epsilon compares all applications
# compare_applications_across_epsilons() which to a single application compares all the epsilons

# Read the CSV file into a DataFrame
actual_df = pd.read_csv('results/real_consumption_sums.csv')

def compare_epsilons_across_applications(muni):
    epsilons = [0.1, 0.3, 0.5, 1, 1.5, 5]

    for epsilon in epsilons:
        print("running epsilon: ", epsilon)
        print("\nrunning NumMunUnbGeoLoc")
        NumMunUnbGeoLoc(epsilon)
        print("\nrunning NumMunUnbGeo")
        NumMunUnbGeo(epsilon)
        NumMunUnbGeoLoc_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
        show_comparison_for_specific_muni([actual_df, NumMunUnbGeoLoc_df, NumMunUnbGeo_df], 
                ['Actual','NumMunUnbGeoLoc', 'NumMunUnbGeo', 'with epsilon: ', epsilon], muni)


def compare_applications_across_epsilons(muni):
    epsilons = [0.1, 0.3, 0.5, 1, 1.5, 5]
    
    plt.figure()
    for epsilon in epsilons:
        NumMun(epsilon)
        df = pd.read_csv('results/NumMun_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMun with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMun and the actual data')
    plt.xlabel('Number of hours in the given period')
    plt.ylabel('Consumption in kWh')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnb(epsilon)
        df = pd.read_csv('results/NumMunUnb_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnb with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnb and the actual data')
    plt.xlabel('Number of hours in the given period')
    plt.ylabel('Consumption in kWh')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnbGeo(epsilon)
        df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnbGeo with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnbGeo and the actual data')
    plt.xlabel('Number of hours in the given period')
    plt.ylabel('Consumption in kWh')
    plt.show()

    plt.figure()
    for epsilon in epsilons:
        NumMunUnbGeoLoc(epsilon)
        df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')
        plt.plot(df[muni], label=f"NumMunUnbGeoLoc with epsilon: {epsilon}")
    plt.plot(actual_df[muni], label="Actual")
    plt.legend()
    plt.title(f'Comparison of {muni} between the dataframe NumMunUnbGeoLoc and the actual data')
    plt.xlabel('Number of hours in the given period')
    plt.ylabel('Consumption in kWh')
    plt.show()


# Outcomment the function you want to run:

compare_applications_across_epsilons('510')
#compare_epsilons_across_applications('510')
