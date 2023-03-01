import json
import os
import sys
from gpsdata_functions import *

def main():
	convert_nmea_to_json()
	
	# Input loop
	while True:
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
			fname = input("Enter file name here: ")
			try:
				commands[int(command)](fname)
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
	
	# Captures 1000 GPS NMEA sentences
	os.system("gpspipe -r -n 100 > nmea_raw.txt")
	
	with open("nmea_raw.txt", "r") as file:
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
		f = open("gpsdata.json","w")
		json.dump(gpsdata_json, f, ensure_ascii=False, indent = 4)
		f.close()
	
	
main()