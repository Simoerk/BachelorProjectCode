import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Experiment that visualize the data from the NumMunUnbGeoLoc and real data

# Read the CSV files into DataFrames
actual_df = pd.read_csv('results/regional_consumption_sums.csv')
result_df = pd.read_csv('results/NumMunUnbGeoLoc_noisy_result.csv')

# Define the regions dictionary
regions = {
        "101": "Hovedstaden",
        "201": "Hovedstaden",
        "151": "Hovedstaden",
        "400": "Hovedstaden",
        "153": "Hovedstaden",
        "155": "Hovedstaden",
        "240": "Hovedstaden",
        "210": "Hovedstaden",
        "147": "Hovedstaden",
        "250": "Hovedstaden",
        "190": "Hovedstaden",
        "157": "Hovedstaden",
        "159": "Hovedstaden",
        "161": "Hovedstaden",
        "270": "Hovedstaden",
        "260": "Hovedstaden",
        "217": "Hovedstaden",
        "163": "Hovedstaden",
        "219": "Hovedstaden",
        "167": "Hovedstaden",
        "169": "Hovedstaden",
        "223": "Hovedstaden",
        "183": "Hovedstaden",
        "165": "Hovedstaden",
        "173": "Hovedstaden",
        "230": "Hovedstaden",
        "175": "Hovedstaden",
        "185": "Hovedstaden",
        "187": "Hovedstaden",
        "320": "Sjaelland",
        "253": "Sjaelland",
        "376": "Sjaelland",
        "316": "Sjaelland",
        "326": "Sjaelland",
        "259": "Sjaelland",
        "350": "Sjaelland",
        "360": "Sjaelland",
        "370": "Sjaelland",
        "306": "Sjaelland",
        "329": "Sjaelland",
        "265": "Sjaelland",
        "330": "Sjaelland",
        "340": "Sjaelland",
        "269": "Sjaelland",
        "336": "Sjaelland",
        "390": "Sjaelland",
        "530": "Syddanmark",
        "561": "Syddanmark",
        "607": "Syddanmark",
        "510": "Syddanmark",
        "621": "Syddanmark",
        "540": "Syddanmark",
        "550": "Syddanmark",
        "573": "Syddanmark",
        "575": "Syddanmark",
        "630": "Syddanmark",
        "580": "Syddanmark",
        "420": "Syddanmark",
        "563": "Syddanmark",
        "430": "Syddanmark",
        "440": "Syddanmark",
        "482": "Syddanmark",
        "410": "Syddanmark",
        "480": "Syddanmark",
        "450": "Syddanmark",
        "461": "Syddanmark",
        "479": "Syddanmark",
        "492": "Syddanmark",
        "710": "Midtjylland",
        "766": "Midtjylland",
        "657": "Midtjylland",
        "661": "Midtjylland",
        "615": "Midtjylland",
        "756": "Midtjylland",
        "665": "Midtjylland",
        "707": "Midtjylland",
        "727": "Midtjylland",
        "730": "Midtjylland",
        "760": "Midtjylland",
        "741": "Midtjylland",
        "740": "Midtjylland",
        "746": "Midtjylland",
        "779": "Midtjylland",
        "671": "Midtjylland",
        "706": "Midtjylland",
        "791": "Midtjylland",
        "751": "Midtjylland",
        "810": "Nordjylland",
        "813": "Nordjylland",
        "860": "Nordjylland",
        "849": "Nordjylland",
        "825": "Nordjylland",
        "846": "Nordjylland",
        "773": "Nordjylland",
        "840": "Nordjylland",
        "787": "Nordjylland",
        "820": "Nordjylland",
        "851": "Nordjylland",
    }

# Function that creates plots of the data
def visualize_data(data):

    df = data

    # Extract relevant columns (municipality numbers)
    municipality_columns = df.columns[1:]

    # Create a new DataFrame to store the region-wise data
    region_data = pd.DataFrame(index=df.index)

    # Map each municipality number to its corresponding region
    for municipality in municipality_columns:
        region = regions.get(municipality)
        if region:
            if region not in region_data:
                region_data[region] = 0
            region_data[region] += df[municipality]

    # Extract unique municipalities for each region
    unique_municipalities = {}
    for region in regions.values():
        if region not in unique_municipalities:
            unique_municipalities[region] = set()
    for municipality, region in regions.items():
        unique_municipalities[region].add(municipality)

    # Plot the data
    for region, data in region_data.items():
        # Get the corresponding unique municipalities for the region
        region_municipalities = sorted(list(unique_municipalities[region]))
        # Aggregate consumption for each municipality across all hours
        aggregated_consumption = [df[municipality].sum() for municipality in region_municipalities]
        plt.plot(region_municipalities, aggregated_consumption, marker='o', label=region)

    plt.xlabel('Municipalities, Regions and DK')
    plt.ylabel('Aggregated Consumption')
    plt.title('Region-wise Aggregated Consumption')
    plt.xticks(rotation=45)
    plt.legend(title='Regions')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Plot the aggregated consumption for each region
def plot_consumption(df1, df2):
    # Extract relevant columns (municipality numbers)
    municipality_columns = df1.columns[1:]

    # Create a new DataFrame to store the region-wise data
    region_data = pd.DataFrame(index=df1.index)

    # Map each municipality number to its corresponding region
    for municipality in municipality_columns:
        region = regions.get(municipality)
        if region:
            if region not in region_data:
                region_data[region] = 0
            region_data[region] += df1[municipality]

    # Extract unique municipalities for each region
    unique_municipalities = {}
    for region in regions.values():
        if region not in unique_municipalities:
            unique_municipalities[region] = set()
    for municipality, region in regions.items():
        unique_municipalities[region].add(municipality)

    # Plot the data from df1
    for region, data in region_data.items():
        # Get the corresponding unique municipalities for the region
        region_municipalities = sorted(list(unique_municipalities[region]))
        # Aggregate consumption for each municipality across all hours
        aggregated_consumption = [df1[municipality].sum() for municipality in region_municipalities]
        plt.plot(region_municipalities, aggregated_consumption, marker='x', label=region)

    # Order df2 columns after regions like df1
    df2_ordered = df2.reindex(columns=df1.columns)

    # Plot the data from df2 (last row as line plot)
    last_row_df2 = df2_ordered.iloc[-1, 1:]  # Extract last row (excluding HourDK column)
    plt.plot(last_row_df2.index, last_row_df2.values, linestyle='', marker='+', label='Total Aggregated Consumption (New Data)')

    plt.xlabel('Municipalities')
    plt.ylabel('Aggregated Consumption')
    plt.title('Region-wise Aggregated Consumption')
    plt.xticks(rotation=45)
    plt.legend(title='Regions')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Plot a bar plot comparing the actual consumption with the noisy consumption
def plot_consumption_barplot(df1, df2):
    # Remove extra columns from df2
    df2 = df2.iloc[:, :len(df1.columns)]

    # Extract relevant columns (municipality numbers)
    municipalities_df2 = df2.columns[1:]  # Exclude first column (HourDK)

    # Reorder columns of df2 to match df1
    df1 = df1.reindex(columns=municipalities_df2)

    # Prepare data for plotting
    consumption_df1 = []
    consumption_df2 = []
    regions_df1 = []

    for municipality in municipalities_df2:
        consumption_df1.append(df1[municipality].iloc[-1])  # Last row value for each municipality in df1
        regions_df1.append(regions.get(municipality, "Regions and DK"))

    for municipality in municipalities_df2:
        consumption_df2.append(df2[municipality].iloc[-1])  # Last row value for each municipality in df2

    # Plot the data
    x = np.arange(len(municipalities_df2))
    bar_width = 0.35

    fig, ax = plt.subplots()

    # Plot df1
    regions_unique = sorted(set(regions_df1))
    color_map = plt.cm.get_cmap('tab10', len(regions_unique))
    for i, region in enumerate(regions_unique):
        indices = [idx for idx, val in enumerate(regions_df1) if val == region]
        ax.bar(x[indices] - bar_width/2, [consumption_df1[idx] for idx in indices], bar_width, label=f'{region} (actual)', color=color_map(i))

    # Plot df2
    ax.bar(x + bar_width/2, consumption_df2, bar_width, color='black', label='with noise')

    # Customize the plot
    ax.set_xlabel('Municipalities, Regions and DK')
    ax.set_ylabel('Consumption')
    ax.set_title('Noisy Consumption Comparison for Each Municipality From 2024-01-21T19:00:00 To 2024-03-31T23:00:00')
    ax.set_xticks(x)
    ax.set_xticklabels(municipalities_df2, rotation=45)
    ax.legend()

    plt.tight_layout()
    plt.show()


def calculate_consumption_difference(df1, df2):
    # Ensure that the dataframes have the same columns and index
    df2 = df2[df1.columns]

    # Remove extra columns from df2
    df2 = df2.iloc[:, :len(df1.columns)]

    # Reorder df2 columns to match df1
    df2 = df2[df1.columns]

    # Calculate the difference for each municipality in each hour
    difference_df = df1.copy()
    difference_df.iloc[:, 1:] = df1.iloc[:, 1:] - df2.iloc[:, 1:]

    return difference_df



plot_consumption_barplot(actual_df, result_df)

#print(calculate_consumption_difference(actual_df, result_df))

#plot_consumption(actual_df, result_df.iloc[:, :-6])

#visualize_data(actual_df)