import pandas as pd
from utils.load_dataset import load_dataset



# Example of adjusting the function to compare relative differences
def compare_datasets(df1, df2):
    common_columns = set(df1.columns).intersection(df2.columns)
    differences_stats = {}
    for column in common_columns:
        if df1[column].dtype.kind in 'biufc' and df2[column].dtype.kind in 'biufc': 
            differences = abs(df1[column] - df2[column])
            relative_differences = (differences / df1[column]) * 100  # percentage differences
            max_difference = relative_differences.max()
            median_difference = relative_differences.median()
            total_difference = relative_differences.sum()
            differences_stats[column] = {
                'max_difference_percent': max_difference,
                'median_difference_percent': median_difference,
                'total_difference_percent': total_difference
            }

    if differences_stats:
        for column, stats in differences_stats.items():
            print(f"{column} - Max % Difference: {stats['max_difference_percent']}, Median % Difference: {stats['median_difference_percent']}, Total % Difference: {stats['total_difference_percent']}")
    else:
        print("No significant differences found or no common numeric columns.")

# This modification calculates the percentage differences which can provide a more normalized view on how significant the differences are in the context of the aggregated sums.


def main():
    # Load datasets
    df_mun1 = load_dataset("results/Num2DUnbGeoLoc_noisy_result.csv", 1000000)
    df_mun2 = load_dataset("results/regional_consumption_sums.csv", 1000000)

    # Compare the datasets
    compare_datasets(df_mun1, df_mun2)

if __name__ == "__main__":
    main()