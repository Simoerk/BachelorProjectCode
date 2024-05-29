import pandas as pd
from utils.muniRegion import *


# Reading the data
NumMunUnbGeo_df = pd.read_csv('results/NumMunUnbGeo_noisy_result.csv')

# Getting the region mapping
region_mapping = give_region()

# Summing the municipalities by region
regions = NumMunUnbGeo_df.columns[1:-5]  # Exclude the date and last 5 columns for regions
region_sums = {region: 0 for region in set(region_mapping.values())}

for municipality in regions:
    region = region_mapping.get(municipality)
    if region:
        region_sums[region] += NumMunUnbGeo_df[municipality].sum()

# Adding the pre-computed regional sums from the dataset for comparison
pre_computed_sums = {
    "Hovedstaden": NumMunUnbGeo_df['Hovedstaden'].sum(),
    "Sjaelland": NumMunUnbGeo_df['Sjaelland'].sum(),
    "Syddanmark": NumMunUnbGeo_df['Syddanmark'].sum(),
    "Midtjylland": NumMunUnbGeo_df['Midtjylland'].sum(),
    "Nordjylland": NumMunUnbGeo_df['Nordjylland'].sum(),
}

# Comparing the calculated sums with the pre-computed sums
comparison_df = pd.DataFrame({
    "Calculated Sum": region_sums,
    "Pre-computed Sum": pre_computed_sums
})

print(comparison_df)