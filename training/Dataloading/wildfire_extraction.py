import csv
import math

def read_coordinates_from_csv(file_path):
    coordinates = []
    names = []
    with open(file_path, 'r', encoding='utf8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            latitude = float(row['Latitude'])
            longitude = float(row['Longitude'])
            name = str(row['Name'])
            distance = math.sqrt((latitude - 39.5624)**2 + (longitude + 120.5635)**2)
            if distance <= 1:
                coordinates.append((latitude, longitude))
                names.append(name)
    return coordinates, names

def write_coordinates_to_txt(coordinates, names, output_file):
    with open(output_file, 'w') as file:
        for i, (lat, lon) in enumerate(coordinates, start=1):
            file.write(f"Number {i}. {names[i-1]}: Latitude {lat}, Longitude {lon}\n")
            file.close
    return coordinates, names

# Example usage
file_path = 'California_Fire_Incidents.csv'
output_file = 'OutputFile.txt'
coordinates, names = read_coordinates_from_csv(file_path)

if coordinates is not None:
    write_coordinates_to_txt(coordinates, names, output_file)
    print(f"Coordinates written to {output_file}")
