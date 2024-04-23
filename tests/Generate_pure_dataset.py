import numpy as np
import pandas as pd
import math
from Mechanisms.BinaryMechanism2DLocal import binary_mechanism_unbounded_local
from utils.laplace import laplace_mechanism
from utils.clipData import *
from utils.clipData import quantileSelection
from utils.muniRegion import give_region
from utils.scale import downScaleDf
from utils.scale import upScaleDf
#from utils.visualizeData import visualize_data

def load_dataset(str): # Function that loads the dataset
    print("Loading the big dataset...")
    data = pd.read_csv(str, nrows=1000000)
    print("Dataset loaded successfully!")
    return data



# Differential privacy on Dataset with Municipality, time and housing/heating category
df_mun = load_dataset("data/muni_data.csv")

# Group by HourDK and MunicipalityNo and sum the ConsumptionkWh
df_mun = df_mun.groupby(['HourDK', 'MunicipalityNo'])['ConsumptionkWh'].sum().reset_index(name='ConsumptionkWh')


#måske fjern
unique_times = sorted(df_mun['HourDK'].unique())


df = df_mun.pivot(index='HourDK', columns='MunicipalityNo', values='ConsumptionkWh')


df = df.cumsum()

#Make processed csv file
df = df.iloc[1:]


#Make processed csv file MÅSKe fJERN?
df.insert(0, 'HourDK', unique_times[1:])


df.to_csv("results/real_consumption_sums.csv.csv", index=False)
print("done")

