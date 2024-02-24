import csv
import math

def read_coordinates_from_csv(file_path):
    coordinates = []
    names = []

    #TODO: open the csv file, read it using csv.DictReader, add coordinates (lat,long) and names to arrays
    #       - remember we want to get fires within a one degree radius of Tahoe (39.5624° N, 120.5635° W) <-- how can we do this?

    return coordinates, names

def write_coordinates_to_txt(coordinates, names, output_file):
    #TODO: create a file named <output_file>, write data into file (hint you can still use the open() function!, do it line by line)

    #see example_output.txt to see formatting (look into python f strings)

    return

# Example usage
file_path = 'California_Fire_Incidents.csv'
output_file = 'output_coordinates.txt'

coordinates, names = read_coordinates_from_csv(file_path)

if coordinates is not None:
    write_coordinates_to_txt(coordinates, names, output_file)
    print(f"Coordinates written to {output_file}")
