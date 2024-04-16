import pandas as pd
import matplotlib.pyplot as plt

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

# Read the CSV file into a DataFrame
df = pd.read_csv('results/processed_data.csv')

# Extract municipality numbers from the HourDK column
df['Municipality'] = df['HourDK'].str.extract(r'(\d+),')

# Map municipality numbers to regions
df['Region'] = df['Municipality'].map(regions).fillna('Unknown')

# Group by region and municipality, then sum the values
grouped = df.groupby(['Region', 'Municipality']).sum()

# Pivot the DataFrame to have regions as columns
pivot_df = grouped.unstack(level=0).fillna(0)

# Plot the data as a stacked bar plot
pivot_df.plot(kind='bar', stacked=True, figsize=(12, 8))
plt.title('Hourly Data by Municipality and Region')
plt.xlabel('Municipality')
plt.ylabel('Sum')
plt.xticks(rotation=45)
plt.legend(title='Region')
plt.grid(axis='y')
plt.tight_layout()
plt.show()
