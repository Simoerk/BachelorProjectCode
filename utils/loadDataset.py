import pandas as pd

# Simple function to load the dataset
def load_dataset(str, n): 
    print("Loading the big dataset...")
    data = pd.read_csv(str, nrows=n)
    print("Dataset loaded successfully!")
    return data