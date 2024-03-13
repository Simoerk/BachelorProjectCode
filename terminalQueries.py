import csv

def load_data(filename):
    """
    Loads data from a CSV file and returns it as a list of dictionaries.
    Each dictionary represents a row in the CSV file.
    """
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def aggregate_consumption_by_hour(data, hour_dk):
    """
    Aggregates consumption based on a specified HourDK.
    """
    total_consumption = 0
    for row in data:
        if row['HourDK'] == hour_dk:
            total_consumption += float(row['ConsumptionkWh'])
    return total_consumption

def main():
    filename = input("Enter the name of the CSV file: ")
    data = load_data(filename)
    print(f"Dataset loaded successfully from {filename}")

    while True:
        query = input("Enter HourDK to aggregate consumption (type 'exit' to quit): ")
        if query.lower() == 'exit':
            print("Exiting...")
            break

        total_consumption = aggregate_consumption_by_hour(data, query)
        print(f"Total consumption for HourDK {query}: {total_consumption} kWh")

if __name__ == "__main__":
    main()
