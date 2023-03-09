import json
import os
import sys

# Name of output files
global GPSDATA_FNAME = "gpsdata.json"
global NMEA_RAW_FNAME = "nmea_raw.txt"

def main():
	convert_nmea_to_json()
	
	print("Press 1 to display all data.")
	print("Press 2 to display longitude and latitude.")
	print("Press 3 to display altitude.")
	print("Press 4 to display geoid altitude")
	print("Press \"q\" to quit.")
		
	# Available helper functions
	commands = {
		1: get_all,
		2: get_lon_lat,
		3: get_alt,
		4: get_geoid_alt,
		"q": sys.exit
	}
		
	command = input(">>> ")
	if command.isnumeric():
		try:
			commands[int(command)](GPSDATA_FNAME)
		except FileNotFoundError:
			print("File is inaccessible.")
			sys.exit(1)
	else:
		try:
			commands[command]()
		except KeyError:
			print("No such command available.")
			sys.exit(1)
			
			
# Captures GPS NMEA sentences, convert them into JSON objects and output to JSON file
def convert_nmea_to_json():
	# Idea: Build a big list of JSON objects and dump all into a JSON file
	gpsdata_json = []
	
	# Captures 100 GPS NMEA sentences
	os.system("gpspipe -r -n 100 > nmea_raw.txt")
	
	with open(NMEA_RAW_FNAME, "r") as file:
		for line in file:
			GPS_DATA = {
				'fixTime': None,
				'Latitude': None,
				'Latitude Direction': None,
				'Longitude': None,
				'Longitude Direction': None,
				'fixQual': None,
				'Number of Satellites': None,
				'HDOP': None,
				'Altitude': None,
				'Altitude Unit': None,
				'geoidAlt': None,
				'geoidAlt Unit': None,
			}			
			sentence = line.split(",")
			
			# The NMEA sentence we need
			if ((sentence[0] == "$GPGGA" or sentence[0] == "$GNGGA")):
				# Build up JSON object containing GPS data
				for i,k in enumerate(['fixTime','Latitude','Latitude Direction','Longitude','Longitude Direction','fixQual','Number of Satellites','HDOP','Altitude','Altitude Unit','geoidAlt','geoidAlt Unit']):				
					GPS_DATA[k]= sentence[i+1]
				gpsdata_json.append(GPS_DATA)
		
		# Writes JSON object list to file
		f = open(GPSDATA_FNAME,"w")
		json.dump(gpsdata_json, f, ensure_ascii=False, indent = 4)
		f.close()
	
# Helper functions for displaying various kinds of GPS data

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

main()
