import pandas as pd

# Simple function to load the dataset
def load_dataset(str, n):
    data = pd.read_csv(str, nrows=n)
    return data