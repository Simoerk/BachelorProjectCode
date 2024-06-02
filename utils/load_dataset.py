import pandas as pd

#simple function to load the dataset
def load_dataset(str, n): 
    print("Loading the big dataset...")
    data = pd.read_csv(str, nrows=n)
    print("Dataset loaded successfully!")
    return data