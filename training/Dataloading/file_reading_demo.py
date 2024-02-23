import csv
import math

#function for reading from a file (puts it into the data array)
def read_from_file(file_path, data):
    with open(file_path, 'r') as file:
        for line in file:
            data.append(line)


# Example usage
data = []
file_path = 'test.txt'
read_from_file(file_path, data)

#printing
counter = 0
for row in data:
    if counter < 5:
        print(row)
    elif counter == 5:
        print("...")
    counter += 1