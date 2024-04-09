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
    

def countDataset(D, start, end):
    left_idx = np.searchsorted(D, start, side='left')
    right_idx = np.searchsorted(D, end, side='right')
    count = right_idx - left_idx
    # Unsure of we are adding the correct noise
    privacy_budget = 0.5
    scale = np.log(np.max(D)) / (2 * privacy_budget)
    noise = np.random.normal(0, scale)
    return count + noise

def quantileSelection (D):
    left = np.min(D)
    right = np.max(D)
    m = 0.999 * np.size(D)
    while left < right:
        mid = np.floor((left + right) / 2)
        c = countDataset(D, np.min(D), mid)
        if c < m:
            left = mid + 1
        else:
            right = mid
    return np.floor((left+right)/2)

def clipData(dataset, clip):
    clipped_dataset = dataset.copy()  # Make a copy of the dataset
    for i in range(np.size(dataset)):
        if dataset[i] > clip:
            clipped_dataset[i] = clip
    return clipped_dataset

def clip(df, column):
    df_column = df[column]
    df_cons_sorted = np.sort(df_column)
    thresh = quantileSelection(df_cons_sorted)
    print(thresh)
    clippedData = clipData(df_column, thresh)
    return clippedData





# def clipData(dataset, clip):
#     for i in range(np.size(dataset)):
#         if dataset[i] > clip:
#             dataset[i] = clip
#     return dataset


# def clip(df, column):
#     df_column = df[column]
#     df_cons_sorted = np.sort(df_column)
#     thresh = quantileSelection(df_cons_sorted)
#     clippedData = clipData(df_column, thresh)
#     return clippedData