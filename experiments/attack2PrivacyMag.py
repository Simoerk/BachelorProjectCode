import pandas as pd

# Load the noisy data from the CSV file
noisy_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')

def calculate_p_sums(noisy_df):
    """
    Calculate the p-sums for each timestep in the binary tree structure.
    
    Parameters:
    noisy_df (pd.DataFrame): DataFrame containing the noisy data.
    
    Returns:
    dict: A dictionary where keys are columns and values are 2D lists with p-sums for each timestep.
    """
    p_sums_dict = {}
    T = len(noisy_df)
    
    for column in noisy_df.columns:
        if column == 'HourDK':
            continue
        
        p_sums = []
        
        for t in range(1, T + 1):
            sums = []
            level = 0
            current_index = t
            
            while current_index <= T:
                step = 1 << level
                if level == 0 and current_index == 1:
                    sums.append(noisy_df[column].iloc[t - 1])
                else:
                    start = current_index
                    end = current_index - step
                    if end < 1:
                        sums.append(noisy_df[column].iloc[start - 1])
                    else:
                        sums.append(noisy_df[column].iloc[start - 1] - noisy_df[column].iloc[end - 1])
                
                 
                current_index += step
                level += 1
            
            p_sums.append(sums)
        
        p_sums_dict[column] = p_sums
    
    return p_sums_dict

# Calculate the p-sums for the dataset
p_sums_dict = calculate_p_sums(noisy_df)

# Display the p-sums for the first column to ensure correctness
first_column = list(p_sums_dict.keys())[0]
for idx, p_sums in enumerate(p_sums_dict[first_column][:5]):
    print(f"Timestep {idx + 1}: {p_sums}")