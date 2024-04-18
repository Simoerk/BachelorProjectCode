import numpy as np
import pandas as pd

# min_val is chosen to be 0 for all functions, because we do not want 
# the lowest value to be 0 after downscaling, which whould happen
# if min_val was the lowest value in the dataset

def downScale(df, col):
    min_val = 0
    max_val = max(df[col])
    df[col] = (df[col] - min_val) / (max_val - min_val)
    return df[col], max_val 

def upScale(df, col, max_val):
    min_val = 0
    df[col] = df[col] * (max_val - min_val) + min_val
    return df[col]

def downScaleDf(df):
    numeric_columns = df.select_dtypes(include='number').columns
    thresh = pd.DataFrame(index=['max_val'], columns=numeric_columns)
    for column in numeric_columns:
        min_val = 0
        max_val = df[column].max()
        df[column] = (df[column] - min_val) / (max_val - min_val)
        thresh[column] = max_val
    return df, thresh

def upScaleDf(df, thresh):
    for column in df.columns.drop('HourDK'):
        if 'max_val' in thresh.index and column in thresh.columns:
            max_val = thresh.loc['max_val', column]
            min_val = 0
            df[column] = df[column] * (max_val - min_val) + min_val
        else:
            print(f"Warning: 'max_val' for '{column}' not found in threshold DataFrame.")
    return df

#data = pd.read_csv("data/test.csv")

#result, thresh = downScaleDf(data)

#result = upScaleDf(result, thresh)
#print("result: ", result)
#print("tresh: ", thresh)
