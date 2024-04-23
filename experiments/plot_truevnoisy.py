import pandas as pd
import matplotlib.pyplot as plt

def load_dataset(file_path):
    """Load dataset from a CSV file."""
    print(f"Loading dataset from {file_path}...")
    data = pd.read_csv(file_path, nrows=1000000)  # Limiting to 1 million rows for large datasets
    print("Dataset loaded successfully!")
    return data

def plot_comparison(true_df, noisy_df, columns, title_prefix=''):
    """
    Plots comparisons between true and noisy data for specified columns.
    Args:
    - true_df (DataFrame): DataFrame containing the true data.
    - noisy_df (DataFrame): DataFrame containing the noisy data.
    - columns (list): List of column names to plot.
    - title_prefix (str): Optional prefix for the plot title to indicate the column.
    """
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


def plot_comparison(true_df, noisy_df, columns, title_prefix=''):
    """
    Plots comparisons between true and noisy data for specified columns, each on a separate subplot.
    Args:
    - true_df (DataFrame): DataFrame containing the true data.
    - noisy_df (DataFrame): DataFrame containing the noisy data.
    - columns (list): List of column names to plot.
    - title_prefix (str): Optional prefix for the plot title to indicate the column.
    """
    # Determine the number of subplots needed
    num_columns = len(columns)
    plt.figure(figsize=(12, num_columns * 4))  # Adjust the figure size as needed

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



def main():
    # Load datasets
    df_mun1 = load_dataset("results/Num2DUnbGeoLoc_noisy_result.csv")
    df_mun2 = load_dataset("results/real_consumption_sums.csv")

    # Convert 'HourDK' to datetime format for better plotting
    df_mun1['HourDK'] = pd.to_datetime(df_mun1['HourDK'])
    df_mun2['HourDK'] = pd.to_datetime(df_mun2['HourDK'])

    # Example usage: Compare specific columns
    columns_to_compare = ['101', '201', '151']  # Add more column IDs based on your interest
    plot_comparison(df_mun1, df_mun2, columns_to_compare, title_prefix='Column')





if __name__ == "__main__":
    main()

