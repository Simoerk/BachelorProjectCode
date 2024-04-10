import requests
import pandas as pd
from datetime import datetime

# Load the existing CSV file into a DataFrame
df_existing = pd.read_csv('../data/muni_data.csv')

# Find the last timestamp in the DataFrame
last_timestamp = pd.to_datetime(df_existing['HourDK']).max()
print(f"Last timestamp in existing data: {last_timestamp}")

# Assuming the API can filter records from a specific start date...
# Convert last_timestamp to a string if required by your API endpoint
start_date_str = last_timestamp.strftime('%Y-%m-%dT%H:%M')

# Fetch new data from the API starting after the last timestamp
response = requests.get(
    url=f'https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?start={start_date_str}'
)
result = response.json()





# Assuming 'records' is the key that contains the data list
new_records = result.get('records', [])
df_new_records = pd.DataFrame(new_records)

# Select the 'ConsumptionkWh' column from the new records
print("Selecting the 'ConsumptionkWh' column from new records...")
sigma_el_new = df_new_records['ConsumptionkWh'].to_numpy()
print("Column selected successfully!")

# Append new records to the existing DataFrame
df_updated = pd.concat([df_new_records, df_existing], ignore_index=True)


# Save the updated DataFrame back to CSV
df_updated.to_csv('../data/muni_data.csv', index=False)
print("Data updated and saved to CSV.")
