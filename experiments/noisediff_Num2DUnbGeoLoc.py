import pandas as pd
from utils.load_dataset import load_dataset

def compare_datasets(df1, df2):
    """Compare two datasets and identify the largest, median, and total differences in each common column,
    including the HourDK of the largest difference and the values that were compared."""
    print("Comparing datasets...")

    # Identify common columns between the two DataFrames, assuming 'HourDK' is not a value to be compared directly
    common_columns = sorted(list(set(df1.columns).intersection(df2.columns) - {'HourDK'}))
    differences_stats = {}

    # Calculate statistical differences for each common column
    for column in common_columns:
        if df1[column].dtype.kind in 'biufc' and df2[column].dtype.kind in 'biufc':  # Check if columns are numeric
            # Calculate absolute differences
            differences = abs(df1[column] - df2[column])
            max_difference = differences.max()  # Find the maximum difference
            max_index = differences.idxmax()  # Get the index of the maximum difference
            max_HourDK = df1.loc[max_index, 'HourDK'] if 'HourDK' in df1.columns else 'HourDK not available'
            value_df1 = df1.loc[max_index, column]
            value_df2 = df2.loc[max_index, column]

            median_difference = differences.median()  # Find the median difference
            total_difference = differences.sum()  # Find the total difference

            # Store the results
            differences_stats[column] = {
                'max_difference': max_difference,
                'max_HourDK': max_HourDK,
                'max_values': {'df1': value_df1, 'df2': value_df2},
                'median_difference': median_difference,
                'total_difference': total_difference
            }

    # Print the results
    if differences_stats:
        print("Differences statistics for each common column:")
        for column, stats in differences_stats.items():
            print(f"{column} - Max difference: {stats['max_difference']} at {stats['max_HourDK']} (Values: df1={stats['max_values']['df1']}, df2={stats['max_values']['df2']}), Median: {stats['median_difference']}, Total: {stats['total_difference']}")
    else:
        print("No significant differences found or no common numeric columns.")

def main():
    # Load datasets
    df_mun1 = load_dataset("results/Num2DUnbGeoLoc_noisy_result.csv", 1000000)
    df_mun2 = load_dataset("results/regional_consumption_sums.csv", 1000000)

    # Compare the datasets
    compare_datasets(df_mun1, df_mun2)

if __name__ == "__main__":
    main()
