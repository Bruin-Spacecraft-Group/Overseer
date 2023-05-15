"""

used to load the wind data by altitude
should be run once before launch
stores in wind.json

*has to be touched

"""

import requests
from datetime import datetime, timedelta
import json
from os import path

# to load in file (assume empty)
# from google.colab import files
# uploaded = files.upload()

filename = 'wind.json'
listObj = []
 
# Check if file exists
if path.isfile(filename) is False:
  raise Exception("File not found")

#want wind speeds across period of time (may change during flight)
flightLength = 3 #expected flight time in hours
time = datetime.utcnow()+ timedelta(hours=-7)     #the start time (uses now, can change later)
time = time - datetime.timedelta(minutes=time.minute % 10,seconds=time.second)  #round for later parsing
timeStart = time.strftime("%Y-%m-%dT%H:%M:%SZ")
timeFin = (time + timedelta(hours=flightLength)).strftime("%Y-%m-%dT%H:%M:%SZ")

#sets rest of parameters
username="ucla_nimmagadda:2FV1aR4qZd" #api username and password (free trial lmao)
timeRange="%s--%s:PT10M" %(timeStart,timeFin)  #time (with given resolution)
location="35,-120_33,-115:15x15"   #lat/long coords

#adds to json for varying altitudes
for alt in range(5, 20000, 1000):
  windSpeed="wind_speed_%dm:ms" %alt
  windDir="wind_dir_%dm:d" %alt
  url="https://" + username + "@api.meteomatics.com/" + timeRange + "/" + windSpeed + "," + windDir + "/" + location + "/json"

  r = requests.get(url).json()
  listObj.append(r)
 
  with open(filename, 'w') as json_file:json.dump(listObj, json_file, indent=4, separators=(',',': '))

  print(url)
  # print(r)
  # print()