import csv
import math

def read_coordinates_from_csv(file_path):
    coordinates = []
    names = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                latitude = float(row['Latitude'])
                longitude = float(row['Longitude'])
                name = str(row['Name'])

                # pythagorean theorem
                c = math.sqrt((latitude - 39.5624)**2 + (longitude + 120.5635)**2)
                if c <= 1:
                    coordinates.append((latitude, longitude))
                    names.append(name)

            except ValueError:
                print(f"Skipping invalid coordinates in row {reader.line_num}")
                continue
            except KeyError:
                print("Error: CSV file must have columns named 'Latitude' and 'Longitude'")
                return None
    return coordinates, names

def write_coordinates_to_txt(coordinates, names, output_file):
    with open(output_file, 'w') as file:
        for i, (lat, lon) in enumerate(coordinates, start=1):
            file.write(f"Number {i}. {names[i-1]}: Latitude {lat}, Longitude {lon}\n")

# Example usage
file_path = 'California_Fire_Incidents.csv'
output_file = 'output_coordinates.txt'

coordinates, names = read_coordinates_from_csv(file_path)

if coordinates is not None:
    write_coordinates_to_txt(coordinates, names, output_file)
    print(f"Coordinates written to {output_file}")
