import pandas as pd
from utils.muniRegion import give_region
from utils.muniRegion import give_regionDictionary

# Let's assume df is your loaded dataframe with municipalities as columns
# HourDK as the index, and the consumption data as the values.

def load_dataset(file_path):
    print("Loading the dataset...")
    data = pd.read_csv(file_path)
    print("Dataset loaded successfully!")
    return data

def map_municipalities_to_regions(df, region_mapping):
    # Melt the DataFrame to work with it more easily
    df_melted = df.melt(id_vars='HourDK', var_name='MunicipalityNo', value_name='ConsumptionkWh')
    
    # Map municipalities to regions
    df_melted['Region'] = df_melted['MunicipalityNo'].map(region_mapping)
    
    return df_melted

def sum_by_region(df_melted):
    # Group by HourDK and Region, then sum the ConsumptionkWh
    df_region_sum = df_melted.groupby(['HourDK', 'Region'])['ConsumptionkWh'].sum().reset_index()
    
    return df_region_sum

def main():
    # Load the dataset
    df = load_dataset("results/test_df.csv")
    
    # Map of municipalities to their regions (based on your provided mappings)
    region_mapping = give_region()

    df_regions = pd.DataFrame()

    # Start by copying the HourDK column
    df_regions['HourDK'] = df['HourDK']
    
    # Transform and map the municipalities to regions
    # For each region, sum the consumptions of the municipalities within that region
    for region, municipalities in give_regionDictionary().items():
        # Sum the consumption for each municipality within the current region
        df_regions[region] = df[municipalities].sum(axis=1)
        
    df_regions = df_regions.iloc[1:]
    df_combined = pd.concat([df, df_regions], axis=1)


    # Save to CSV if needed
    df_combined.to_csv("results/regional_consumption_sums.csv", index=False)

if __name__ == "__main__":
    main()
