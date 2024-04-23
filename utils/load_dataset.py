import pandas as pd

def load_dataset(str, n): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv(str, nrows=n)
    print("Dataset loaded successfully!")
    return data