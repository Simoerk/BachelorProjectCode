import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_consumption_barplot(real_df):

    # Extract municipality numbers
    municipalities = real_df.columns[1:]

    # Get consumption values for the last hour
    consumption_values = [real_df[municipality].iloc[-1] for municipality in municipalities]

    # Plotting
    plt.figure(figsize=(12, 8))
    plt.bar(municipalities, consumption_values, color='blue')
    plt.xlabel('Municipality')
    plt.ylabel('Consumption')
    plt.title('Real Consumption Data by Municipality')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
