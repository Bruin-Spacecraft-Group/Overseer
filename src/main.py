from time import sleep
import csv
from gpiozero import OutputDevice
from subprocess import Popen, PIPE, STDOUT

'''
# geofence
import prediction as pred
import landing_prediction as land
from shapely.geometry import Point, Polygon
'''

# removed asyncio - will run global connection in seperate terminal

# global data collection (json)
# json_cmd = "gpspipe -w | fgrep TPV > master.log"

# GLOBAL CONSTANTS
csv_cmd = "gpscsv -n 1 -f time,lat,lon,alt,altHAE,altMSL,climb,speed,epc,epx,epy,epv,eps,velD,velE,velN > output.csv"
run = True
MAX_ALT = 22000

# manual cutdown (endless signal)
def cutdown():
    pin = OutputDevice(4)
    pin.on()
    sleep(120)
    pin.off()
    run = False

'''
# True if within redzone
def geofence(time, lat, lon, altitude):
    pred = pred.Predictor(22000, 1.0)
    zones = land.createZones()

    # check if at red zone
    def inZone(current):
        for shape in zones:
            if current.within(zones[shape]):
                return True
        return False

    # update predictor
    def update(c):
        pred.AddGPSPosition(c)
        return Point(pred.PreviousPosition["lat"], pred.PreviousPosition["lon"])

    # core output
    pos = {
        "time": time,
        "lat": lat,
        "lon": lon,
        "alt": altitude,
        "sats": pred.PreviousPosition["sats"],
        "fixtype": pred.PreviousPositon["fixtype"],
    }
    if inZone(update(pos)):
        return True
    else:
        return False
'''

# position checking for cutdown
def main():
    while run:
        # load csv data
        ps = Popen(csv_cmd, shell=True, stdout=PIPE, stderr=STDOUT)
        output = ps.communicate()[0]
        # rotating data vals
        (
            time,
            lat,
            lon,
            alt,
            altHAE,
            altMSL,
            climb,
            speed,
            epc,
            epx,
            epy,
            epv,
            eps,
            velD,
            velE,
            velN,
        ) = (
            "",
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
        )
        # csv parsing
        try:
            with open("output.csv", "r") as f:
                reader = csv.reader(f)
                reader.next()
                for row in reader:
                    time,lat,lon,alt,altHAE,altMSL,climb,speed,epc,epx,epy,epv,eps,velD,velE,velN = (
                        row[0],
                        float(row[1]),
                        float(row[2]),
                        float(row[3]),
                        float(row[4]),
                        float(row[5]),
                        float(row[6]),
                        float(row[7]),
                        float(row[8]),
                        float(row[9]),
                        float(row[10]),
                        float(row[11]),
                        float(row[12]),
                        float(row[13]),
                        float(row[14]),
                        float(row[15])
                    )
            print(time,lat,lon,alt,altHAE,altMSL,climb,speed,epc,epx,epy,epv,eps,velD,velE,velN)
            with open("master.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow(
                    [
                        time,
                        lat,
                        lon,
                        alt,
                        altHAE,
                        altMSL,
                        climb,
                        speed,
                        epc,
                        epx,
                        epy,
                        epv,
                        eps,
                        velD,
                        velE,
                        velN,
                    ]
                )
        except:
            sleep(5)
        # call cutdown
        if alt >= MAX_ALT:
            cutdown()
        else:
            sleep(5)


# run
main()
