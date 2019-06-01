import time
import geofencev2 as gf
#import cutdown as cd
#import ReceiveData as rd
import currCoords as coords
import datetime
import sys
# MODIFY THESE!!! to be the location of said data within data file string

count=0
check_file = open("checkCoords.csv", "w+")
log_file = open("flightLog.txt", "w+")

# Can either do 30s loop or continuous

while(True):
	#all_data = open("datafilehere.csv", "r")
	#latest_data = all_data.readline()
	#latit, longit = latest_data[LATITUDE], latest_data[LONGITUDE]
	#all_data.close()
	#latit, longit = 34.06868, -118.44331
	#latit, longit = 34.614549, -118.560853
	latit, longit = 34.542620, -117.883676
	#latit, longit = tm.Find_Latest_Coordinate()
	check_file.write(str(datetime.datetime.now()) + ", " + str(latit) + ", " + str(longit) + "\n")
	if (gf.checkSafety(latit, longit)):
		count = count + 1
		# log info this line
		log_file.write(str(datetime.datetime.now()) + " Right into the Danger Zone!" + "\n")
		#print("ERROR")
	else:
		count = 0
		#print("SAFETY")
		log_file.write(str(datetime.datetime.now()) + " In the Safety Zone!" + "\n")
		#sleep(30)
	if count > 20:
		# signal failsafe.py
		# log this
		#cd.cut_down()
		log_file.write(str(datetime.datetime.now()) + " Cutting down...Executing cutdown.py")
		print("CUTDOWN")
		sys.exit()

check_file.close()
log_file.close()

	# read latest GPS coords from file -> (longit, latit)
	# store these coords to a separate file
	# check with geofence to see if in-out -> send result to log.py
	# if geofence=false > 5 then signal to failsafe.py to cut -> log it
