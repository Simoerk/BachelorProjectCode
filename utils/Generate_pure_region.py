import pandas as pd
from utils.muniRegion import give_region
from utils.muniRegion import give_regionDictionary
from utils.load_dataset import load_dataset

# util to generate a dataset with the cumulative sum of the real consumption data from Energinet
# with regions

def map_municipalities_to_regions(df, region_mapping):
    df_melted = df.melt(id_vars='HourDK', var_name='MunicipalityNo', value_name='ConsumptionkWh')
    df_melted['Region'] = df_melted['MunicipalityNo'].map(region_mapping)
    return df_melted

def sum_by_region(df_melted):
    df_region_sum = df_melted.groupby(['HourDK', 'Region'])['ConsumptionkWh'].sum().reset_index()
    return df_region_sum

def main():
    df = load_dataset("results/real_consumption_sums.csv", 1000000)
    
    df_regions = pd.DataFrame()
    df_regions['HourDK'] = df['HourDK']
    
    # Dictionary to store all municipalities in each region
    region_dict = give_regionDictionary()

    # Sum the consumptions for each region
    for region, municipalities in region_dict.items():
        df_regions[region] = df[municipalities].sum(axis=1)
    
    # Add a 'DK' column that sums all regional consumptions
    df_regions['DK'] = df_regions[list(region_dict.keys())].sum(axis=1)

    # Combine the original dataframe with the new regions dataframe
    df_combined = pd.concat([df, df_regions.drop(df_regions.columns[0], axis=1)], axis=1)

    # Save the combined DataFrame to CSV
    df_combined.to_csv("results/regional_consumption_sums.csv", index=False)

if __name__ == "__main__":
    main()
