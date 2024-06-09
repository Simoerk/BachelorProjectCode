import requests
import pandas as pd

# Util to extract data from Energinet's API

print("This might take a couple of minutes...")

response = requests.get(
    url='https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?limit=1000000')

result = response.json()

records = result.get('records', [])                                  

df_records = pd.DataFrame(records)

# Save the data to a CSV file
df_records.to_csv('./data/muni_data.csv', index=False)