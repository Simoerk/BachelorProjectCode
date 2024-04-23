import pandas as pd

def load_dataset(file_path):
    """Load dataset from a CSV file."""
    print(f"Loading dataset from {file_path}...")
    data = pd.read_csv(file_path, nrows=1000000)  # Limiting to 1 million rows for large datasets
    print("Dataset loaded successfully!")
    return data

def compare_datasets(df1, df2):
    """Compare two datasets and identify the largest, median, and total differences in each common column,
    including the HourDK of the largest difference."""
    print("Comparing datasets...")

    # Identify common columns between the two DataFrames, assuming 'HourDK' is not a value to be compared directly
    common_columns = set(df1.columns).intersection(df2.columns) - {'HourDK'}
    differences_stats = {}

    # Calculate statistical differences for each common column
    for column in common_columns:
        if df1[column].dtype.kind in 'biufc' and df2[column].dtype.kind in 'biufc':  # Check if columns are numeric
            # Calculate absolute differences
            differences = abs(df1[column] - df2[column])
            max_difference = differences.max()  # Find the maximum difference
            max_index = differences.idxmax()  # Get the index of the maximum difference
            max_HourDK = df1.loc[max_index, 'HourDK'] if 'HourDK' in df1.columns else 'HourDK not available'

            median_difference = differences.median()  # Find the median difference
            total_difference = differences.sum()  # Find the total difference

            # Store the results
            differences_stats[column] = {
                'max_difference': max_difference,
                'max_HourDK': max_HourDK,
                'median_difference': median_difference,
                'total_difference': total_difference
            }

    # Print the results
    if differences_stats:
        print("Differences statistics for each common column:")
        for column, stats in differences_stats.items():
            print(f"{column} - Max: {stats['max_difference']} at {stats['max_HourDK']}, Median: {stats['median_difference']}, Total: {stats['total_difference']}")
    else:
        print("No significant differences found or no common numeric columns.")

def main():
    # Load datasets
    df_mun1 = load_dataset("results/result_Num2DGeoLocal_df.csv")
    df_mun2 = load_dataset("results/test_df.csv")

    # Compare the datasets
    compare_datasets(df_mun1, df_mun2)

if __name__ == "__main__":
    main()
