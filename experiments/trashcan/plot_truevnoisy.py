import pandas as pd
import matplotlib.pyplot as plt

# Experiment to compare the summary statistics of the actual and noisy datasets

def load_dataset(file_path):
    """Load dataset from a CSV file."""
    print(f"Loading dataset from {file_path}...")
    data = pd.read_csv(file_path, nrows=1000000)  # Limiting to 1 million rows for large datasets
    print("Dataset loaded successfully!")
    return data

# Plots the comparison between true and noisy data for specified columns
def plot_comparison(true_df, noisy_df, columns, title_prefix=''):
    
    plt.figure(figsize=(12, 8))
    
    # Plot each column.
    for column in columns:
        if column in true_df.columns and column in noisy_df.columns:
            plt.plot(true_df['HourDK'], true_df[column], label=f'True {column}')
            plt.plot(noisy_df['HourDK'], noisy_df[column], label=f'Noisy {column}', linestyle='--')
    
    plt.title(f'{title_prefix} True vs. Noisy Data Comparison')
    plt.xlabel('HourDK')
    plt.ylabel('Sum')
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Plots the comparison between true and noisy data for specified columns
def plot_comparison(true_df, noisy_df, columns, title_prefix=''):

    # Determine the number of subplots needed
    num_columns = len(columns)
    plt.figure(figsize=(12, num_columns * 4)) # Adjust height based on number of columns

    for i, column in enumerate(columns):
        if column in true_df.columns and column in noisy_df.columns:
            ax = plt.subplot(num_columns, 1, i+1)  # Create a subplot for each column
            ax.plot(true_df['HourDK'], true_df[column], label=f'True {column}')
            ax.plot(noisy_df['HourDK'], noisy_df[column], label=f'Noisy {column}', linestyle='--')
            ax.set_title(f'{title_prefix} {column} - True vs. Noisy Data')
            ax.set_xlabel('HourDK')
            ax.set_ylabel('Sum')
            ax.legend()
            ax.xaxis.set_major_locator(plt.MaxNLocator(10))  # Limit number of x-ticks
            plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

# Main function to run the comparison
def main():
    # Load datasets
    df_mun1 = load_dataset("results/Num2DUnbGeoLoc_noisy_result.csv")
    df_mun2 = load_dataset("results/real_consumption_sums.csv")

    # Convert 'HourDK' to datetime format for better plotting
    df_mun1['HourDK'] = pd.to_datetime(df_mun1['HourDK'])
    df_mun2['HourDK'] = pd.to_datetime(df_mun2['HourDK'])

    columns_to_compare = ['101', '201', '151'] # Specify columns to compare
    plot_comparison(df_mun1, df_mun2, columns_to_compare, title_prefix='Column')

# Main function runs when the file is executed
if __name__ == "__main__":
    main()

