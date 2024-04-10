
#while
    #try: 
    #    open result_df.csv
    #    last_data = pd.read_csv("results/result_df.csv")
    #    last_datetime = last_result['HourDK'].max()
    #    response = requests.get(
    #           url=f'https://api.energidataservice.dk/dataset/PrivIndustryConsumptionHour?start={start_date_str}'
    #    )
    #    new_data = response.json()
    #    if new_data['HourDK'] > last_datetime:
    #        Numerical2DupdaterUnb.py
    #except:
    #    Numerical2DinitialUnb.py