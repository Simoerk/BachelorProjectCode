import numpy as np
import pandas as pd
import math
from utils.laplace import laplace_mechanism

# def countDataset(D, start, end):
#     count = 0
#     for i in range(np.size(D)):
#         if D[i] >= start and D[i] <= end:
#             count += 1
#     return count
    
# Adds noise to the count of the dataset from start to mid
def noisyCount(D, start, end, epsilon):
    count = end - start
    # Unsure of we are adding the correct noise
    #privacy_budget = 0.5
    #scale = np.log(np.max(D)) / (2 * privacy_budget)
    #scale = np.log(len(D)) / (2 * privacy_budget)
    #noise = np.random.normal(0, scale)
    #noise = laplace_mechanism(1, 1)
    scale = math.log2(len(D)) / (epsilon)
    noise = np.random.laplace(0, scale)
    return count + noise

# Threshold is decided privately
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
    thresh = quantileSelection(df_cons_sorted, 0.99 * np.size(df_cons_sorted), epsilon)
    clippedData = clipData(df_column, thresh)
    return clippedData, thresh



def clip_pr_column(df, epsilon):
    thresh_list = []
    for column in df.columns:
        if column != 'HourDK':
            df[column], thresh = clip(df, column, epsilon)
            thresh_list.append(thresh)
    return df, thresh_list

#data = [21, 123, 213, 276, 282, 323, 374, 424, 488, 523, 576, 628, 698, 734, 784, 1239, 1419, 12302, 102329]

#print(quantileSelection(data, 0.999 * np.size(data)))