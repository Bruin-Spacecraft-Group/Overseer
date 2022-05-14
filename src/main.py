import time
from subprocess import call

call(["gpspipe","-w","|","fgrep","TPV",">","master.log"])

while True:
  call(["gpscsv","-n","2","-f","time,lat,lon,alt",">","output.csv"])
  with open("output.csv", "r") as f:
    writer = csv.writer(f)
  
  
  sleep(5)
