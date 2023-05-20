
import json, subprocess

# capture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]

def gps():
  rets = list(2)
  with open("gps_data.json", "w") as f:
    subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
  with open("gps_data.json", "r") as f:
    gps_data = []
    for line in f:
      json_loaded = json.loads(line)
      if json_loaded["class"] == "TPV":
        rets[0] = json_loaded
        break
  return rets


print(gps()[0])