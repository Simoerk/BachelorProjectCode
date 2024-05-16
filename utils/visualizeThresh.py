import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from clipData import clip

# Load datasets
real_df = pd.read_csv('results/real_consumption_sums.csv')

# Clip the data to remove outliers
for col in real_df.columns[1:]:
    real_df[col] = clip(real_df[col], 0.1, 0.9)