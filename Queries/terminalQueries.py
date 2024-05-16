import os
import pandas as pd

def aggregate_consumption_by_interval(df, municipality_numbers, start_time, end_time):
    
    municipality_numbers_list = municipality_numbers.split(",")
    total_con = 0

    for municipality_number in municipality_numbers_list:
        df_timefiltered = df[(df['HourDK'] >= start_time) & (df['HourDK'] <= end_time)]
        consumption_in_interval = df_timefiltered.loc[df_timefiltered['HourDK'] == end_time, municipality_number].values[0] - df_timefiltered.loc[df_timefiltered['HourDK'] == start_time, municipality_number].values[0]
        total_con += consumption_in_interval
        
    return total_con

def main():
    # Get the directory path for the queries folder
    queries_folder = 'queries'
    # Get the directory path for the results folder
    results_folder = os.path.join('..', 'results')  # Navigate out of the current folder

    # Construct the file path for the DataFrame
    dataframe_path = os.path.join(results_folder, 'result.csv')
    
    # df = pd.read_csv(dataframe_path)
    
    df = pd.read_csv("results/NumMunUnbGeoLoc_noisy_result.csv")

    print("DataFrame loaded successfully.")

    while True:
        municipality_number = str(input("Enter the municipality numbers: "))
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




#municipalities_str = [str(mun) for mun in municipalities]  # Use this line if necessary
#columns_to_select = ['Time'] + municipalities_str