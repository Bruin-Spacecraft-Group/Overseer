from time import sleep
import csv
from gpiozero import OutputDevice
from subprocess import Popen, PIPE, STDOUT

# removed asyncio - will run global connection in seperate terminal

# global data collection (json)
#   json_cmd = "gpspipe -w | fgrep TPV > master.log"

# rotating csv data
csv_cmd = "gpscsv -n 1 -f time,lat,lon,alt > output.csv"

run = True
# manual cutdown (endless signal)
def cutdown():
  pin = OutputDevice(4)
  pin.on()
  run = False

# position checking for cutdown
def main():
  while run:
    # load csv data
    ps = Popen(csv_cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    output = ps.communicate()[0]

    # rotating data vals
    time, lat, lon, alt = "",0.0,0.0,0.0

    # csv parsing
    with open("output.csv", "r") as f:
      reader = csv.reader(f)
      for row in reader:
        time, lat, lon, alt = row[0], float(row[1]), float(row[2]), float(row[3])
    
    # pass data to geofence
    

    sleep(5)


# run
main()


