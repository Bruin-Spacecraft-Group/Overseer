import time
import thread
import geofence

# MODIFY THESE!!! to be the location of said data within data file string
LATITUDE = 1
LONGITUDE = 2

count=0
check_file = open("check_coords.csv", "w+")

# Can either do 30s loop or continuous

while(True):
    thing = open("datafilehere.csv", "r")
    latest_data = thing.readline()
    latit, longit = latest_data[LATITUDE], latest_data[LONGITUDE]
    thing.close()
    # latit, longit = 34.06868, -118.44331     --> dummy
    check_file.write(str(longit), ",", str(latit), ",\n")
    if (inorout(latit, longit)):
        count = count + 1
        # log info this line
    else:
        count = 0
    if count > 5:
        # signal failsafe.py
        # log this


check_file.close()

    # read latest GPS coords from file -> (longit, latit)
    # store these coords to a separate file
    # check with geofence to see if in-out -> send result to log.py
    # if geofence=false > 5 then signal to failsafe.py to cut -> log it
