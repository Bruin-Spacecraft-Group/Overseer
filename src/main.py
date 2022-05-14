import asyncio
import csv
from gpiozero import OutputDevice
from subprocess import call

# global data collection (json)
call(["gpspipe","-w","|","fgrep","TPV",">","master.log"])

# manual cutdown
async def cutdown():
  pin = OutputDevice(4)
  pin.on()
  asyncio.sleep(120)
  pin.off()

# data parsing (csv)
async def data():
  while True:
    call(["gpscsv","-n","2","-f","time,lat,lon,alt",">","output.csv"])
    with open("output.csv", "r") as f:
      reader = csv.reader(f)
      next(reader)

