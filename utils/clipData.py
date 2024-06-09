import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism
import warnings

warnings.filterwarnings('ignore', category=FutureWarning, message=".*Series.__getitem__ treating keys as positions is deprecated.*")

# Adds noise to the count of the dataset from start to mid
def noisyCount(D, start, end, epsilon):
    count = end - start
    scale = math.log2(len(D)) / (epsilon)
    noise = np.random.laplace(0, scale)
    return count + noise

# Function that decides threshold privately with binary search  
def quantileSelection(D, m, epsilon):
    left = 0
    right = len(D)-1
    while left < right:
        mid = np.floor((left + right) / 2)
        c = noisyCount(D, 0, mid, epsilon)
        if c < m:
            left = mid + 1
        else:
            right = mid
    thresh = D[int(np.floor((left+right)/2))]
    return thresh

# Uses threshold to clip a dataset
def clipData(dataset, thresh):
    clipped_dataset = dataset.copy()  # Make a copy of the dataset
    for i in range(np.size(dataset)):
        if dataset[i] > thresh:
            clipped_dataset[i] = thresh
    return clipped_dataset

# Calls quantileSelection and clipData to select threshold and clip the data
def clip(df, column, epsilon):
    df_column = df[column]
    df_cons_sorted = np.sort(df_column)
    # Threshold is set to the 99.9% quantile
    thresh = quantileSelection(df_cons_sorted, 0.999 * np.size(df_cons_sorted), epsilon)
    clippedData = clipData(df_column, thresh)
    return clippedData, thresh

# Clips all columns in a dataset using the clip function
def clip_pr_column(df, epsilon):
    thresh_list = []
    for column in df.columns:
        if column != 'HourDK':
            df[column], thresh = clip(df, column, epsilon)
            thresh_list.append(thresh)
    return df, thresh_list
