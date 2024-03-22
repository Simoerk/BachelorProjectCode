import os
import pandas as pd

def aggregate_consumption_by_interval(df, municipality_number, start_time, end_time):
    """
    Aggregates consumption for a specified municipality number within a given time interval.
    """
    mask = (df['MunicipalityNumber'] == municipality_number) & \
           (df['Time'] >= start_time) & \
           (df['Time'] <= end_time)
    consumption_in_interval = df.loc[mask, 'ElectricityConsumption'].sum()
    return consumption_in_interval

def main():
    # Get the directory path for the results folder
    results_folder = os.path.join('..','results')
    
    # Construct the file path for the DataFrame
    dataframe_path = os.path.join(results_folder, 'result.csv')

    df = pd.read_csv(dataframe_path)

    print("DataFrame loaded successfully.")

    while True:
        municipality_number = int(input("Enter the municipality number: "))
        start_time = input("Enter the start time (YYYY-MM-DDTHH:MM:SS format): ")
        end_time = input("Enter the end time (YYYY-MM-DDTHH:MM:SS format): ")

        consumption_in_interval = aggregate_consumption_by_interval(df, municipality_number, start_time, end_time)
        print(f"Total consumption for Municipality {municipality_number} between {start_time} and {end_time}: {consumption_in_interval} kWh")

        exit_choice = input("Do you want to exit? (yes/no): ").lower()
        if exit_choice == 'yes':
            print("Exiting...")
            break

if __name__ == "__main__":
    main()
