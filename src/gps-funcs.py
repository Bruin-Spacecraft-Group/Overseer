# Helper functions for printing various kinds of GPS data
import json
import sys

# Prints all GPS data
def get_all(file):
	with open(file, "r") as file:
		data = json.load(file)
		for item in data:
			for key in item:
				print(f'{key}: ', item[key])
			print("\n")
	sys.exit(0)

# Prints only longitude and latitude, with directions
def get_lon_lat(file):
	with open(file, "r") as file:
		data = json.load(file)
		for item in data:
			print("Longitude: ", item["Longitude"])
			print("Longitude Direction: ", item["Longitude Direction"])
			print("Latitude: ", item["Latitude"])
			print("Latitude Direction: ", item["Latitude Direction"])
			print("\n")
	sys.exit(0)
		
# Prints altiude
def get_alt(file):
	with open(file, "r") as file:
		data = json.load(file)
		for item in data:
			print("Altitude: ", item['Altitude'])
			print("Altitude Unit: ", item['Altitude Unit'])
			print("\n")
	sys.exit(0)

# Prints geoid altitude
def get_geoid_alt(file):
	data = json.load(file)
	for item in data:
		print("Geoid Altitude: ", item['geoidAlt'])
		print("Geoid Altitude Unit: ", item['geoidAlt Unit'])
		print("\n")
	sys.exit(0)
	
# Prints fix quality
def get_fix_qual(file):
	data = json.load(file)
	for item in data:
		if item['fixQual'] == 1:
			print("Fix quality: GPS")
		elif item['fixQual'] == 2:
			print("Fix Quality: DGPS")
		else:
			print("Invalid fix quality")
		print("\n")
	sys.exit(0)