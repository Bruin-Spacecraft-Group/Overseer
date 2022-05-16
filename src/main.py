from time import sleep
import csv
from gpiozero import OutputDevice
from subprocess import Popen, PIPE, STDOUT

# geofence
from prediction import createZones, Predictor
from shapely.geometry import Point, Polygon



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


def geofence(time, lat, lon, altitude):
    pred = Predictor(40000, 17.5)
    zones = createZones()

    # check if at red zone
    def inZone(current):
        for shape in zones:
            if current.within(zones[shape]):
                return True
        return False

    # update predictor
    def update(c):
        pred.AddGPSPosition(c)
        return Point(pred.PreviousPosition['lat'], pred.PreviousPosition['lon'])

    # main loop; must feed in new positions
    stop = 0
    while True:
        pos = {'time': time, 'lat': lat, 'lon': lon, 'alt': altitude, 'sats': pred.PreviousPosition['sats'], 'fixtype': pred.PreviousPositon['fixtype']}
        
        while altitude < pred.MaximumAltitude: #not yet at max altitude
            continue
        while inZone(update(pos)):
            continue 
        while True: # the balloon is in a white zone and also above max altitude
            if inZone(update(pos)):
                cutdown()
                stop = 1
                break
        if stop:
            break

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


