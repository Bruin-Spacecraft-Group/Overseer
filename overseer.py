import time
import thread
import geofence as gf
import cutdown as cd
import ReceiveData as rd


# MODIFY THESE!!! to be the location of said data within data file string
LATITUDE = 1
LONGITUDE = 2

ERROR_VALUE = 99

count=0

# Can either do 30s loop or continuous

while(True):
    inputVal = input()
    retVal = rd.data_receive_callback(inputVal)

    if retVal == ERROR_VALUE:
        cd.cut_down()
