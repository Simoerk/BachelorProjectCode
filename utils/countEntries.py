import pandas as pd

# Util to count entries in the dataset

# Read the CSV file into a DataFrame
df = pd.read_csv("muni_data.csv")

# Convert HourUTC to datetime format
df['HourUTC'] = pd.to_datetime(df['HourUTC'])

# Group by HourUTC and MunicipalityNumber and count the number of cases
hourly_counts = df.groupby(['HourUTC', 'MunicipalityNo']).size().reset_index(name='Count')

# Check if every hour contains exactly 10 cases for every municipality number
for hour in hourly_counts['HourUTC'].unique():
    for municipality in df['MunicipalityNo'].unique():
        if (hourly_counts[(hourly_counts['HourUTC'] == hour) & (hourly_counts['MunicipalityNo'] == municipality)]['Count'] != 10).any():
            print(f"At {hour}, Municipality {municipality} does not have exactly 10 cases of consumption.")
        else:
            print(f"At {hour}, Municipality {municipality} has exactly 10 cases of consumption.")
