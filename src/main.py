import asyncio
import csv
from gpiozero import OutputDevice
from subprocess import Popen, PIPE, STDOUT

# global data collection (json) uh
json_cmd = "gpspipe -w | fgrep TPV > master.log"
csv_cmd = "gpscsv -n 1 -f time,lat,lon,alt > output.csv"

# call(["gpspipe","-w","|","fgrep","TPV",">","master.log"])

# manual cutdown
async def cutdown():
  pin = OutputDevice(4)
  pin.on()
  asyncio.sleep(120)
  pin.off()

# data parsing (csv)
async def data():
  while True:
    ps = Popen(csv_cmd, shell=True, stdout=PIPE, stderr=STDOUT)
    output = ps.communicate()[0]
    with open("output.csv", "r") as f:
      reader = csv.reader(f)
      next(reader)

asyncio.run(data())


