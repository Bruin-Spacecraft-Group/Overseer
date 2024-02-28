import csv
import math

def read_coordinates_from_csv(file_path):
    coordinates = []
    names = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                #TODO: get the latitude, longitude, and name columns
                #TODO: calculate distance between each row and tahoe (lat:39.5624, long:120.5635), if distance <= 1 add to arrays
                pass #TODO: delete this line once you enter your implementation

            except ValueError:
                print(f"Skipping invalid coordinates in row {reader.line_num}")
                continue
            except KeyError:
                print("Error: CSV file must have columns named 'Latitude' and 'Longitude'")
                return None
    return coordinates, names

def write_coordinates_to_txt(coordinates, names, output_file):
    with open(output_file, 'w') as file:
        #TODO: iterate throught coordinates and names and file.write(f"...")
        pass #TODO: delete this line once you enter your implementation

# Example usage
file_path = 'California_Fire_Incidents.csv'
output_file = 'output_coordinates.txt'

coordinates, names = read_coordinates_from_csv(file_path)

if coordinates is not None:
    write_coordinates_to_txt(coordinates, names, output_file)
    print(f"Coordinates written to {output_file}")
