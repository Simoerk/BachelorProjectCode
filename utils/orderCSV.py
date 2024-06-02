import csv

# Function to sort a CSV file by a specific column
def sort_csv(input_file, output_file):
    # Read the CSV file and store its rows in a list
    with open(input_file, 'r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = [row for row in csv_reader]

    # Sort the data by the "number" column
    sorted_data = sorted(data, key=lambda x: int(x['number']))

    # Write the sorted data to a new CSV file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['name', 'number']
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header
        csv_writer.writeheader()
        
        # Write the sorted rows
        csv_writer.writerows(sorted_data)

# Replace 'input.csv' and 'output.csv' with your actual file names
input_file = 'Municipality.csv'
output_file = 'orderedMunicipality.csv'

sort_csv(input_file, output_file)
