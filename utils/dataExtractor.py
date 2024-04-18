import requests
import pandas as pd

response = requests.get(
    url='https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?limit=2000000')

result = response.json()

#for k, v in result.items():
#    print(k, v)

records = result.get('records', [])
                                           
#print('records:')
#for record in records:
#    print(' ', record)


df_records = pd.DataFrame(records)

# Select the 'Diabetes_binary' column as a numpy array
print("Selecting the 'ConsumptionkWh' column...")
sigma_el = df_records['ConsumptionkWh'].to_numpy()
print("Column selected successfully!")

df_records.to_csv('./data/muni_data.csv', index=False)