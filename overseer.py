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
latit, longit = 10, 25
while(True):
    
    latit = gf.increment(latit)
    longit = gf.increment(longit)
    #all_data = open("datafilehere.csv", "r")
    #latest_data = all_data.readline()
    #latit, longit = latest_data[LATITUDE], latest_data[LONGITUDE]
    #all_data.close()
    #latit, longit = 34.06868, -118.44331
    #latit, longit = 34.614549, -118.560853
    #latit, longit = tm.Find_Latest_Coordinate()
    check_file.write(str(datetime.datetime.now()) + ", " + str(latit) + ", " + str(longit) + "\n")

    if (gf.inDangerZone(latit, longit)):
        count = count + 1
    # Log info in this line
        log_file.write(str(datetime.datetime.now()) + " Right into the Danger Zone!" + "\n")
        print("ERROR")
	time.sleep(1) # adding 1 second delay
    else:
        count = 0 # if in safety zone reset to 0
        print("SAFETY")
        log_file.write(str(datetime.datetime.now()) + " In the Safety Zone!" + "\n")
	time.sleep(1) # adding 1 second delay
    #sleep(30)
    if count > 60: # if it has been in the danger zone for longer than 60 seconds signal failsafe
        # Signal failsafe.py
    # Log this
    #cd.cut_down()
        log_file.write(str(datetime.datetime.now()) + " Cutting down...Executing cutdown.py")
        print("CUTDOWN")
        sys.exit()
    time.sleep(0.5)
check_file.close()
log_file.close()

	# Read latest GPS coords from file -> (longit, latit)
	# Store these coords to a separate file
	# Check with geofencev2.py to see if the coords are in or out of the Safety Zone -> send result to log.py
	# If geofence=false > 5 then signal to failsafe.py to cut -> log it
