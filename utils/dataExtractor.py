import requests
import pandas as pd

# Util to extract data from Energinet's API

response = requests.get(
    url='https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?limit=2000000')

result = response.json()

records = result.get('records', [])                                  

df_records = pd.DataFrame(records)

# Select the 'ConsumptionkWh' column
print("Selecting the 'ConsumptionkWh' column...")
sigma_el = df_records['ConsumptionkWh'].to_numpy()
print("Column selected successfully!")

# Save the data to a CSV file
df_records.to_csv('./data/muni_data.csv', index=False)