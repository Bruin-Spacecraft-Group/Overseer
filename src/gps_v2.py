
import json, subprocess

# capture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]

def gps():
  with open("gps_data.json", "w") as f:
    subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
  with open("gps_data.json", "r") as f:
    gps_data = dict()
    for line in f:
      json_loaded = json.loads(line)
      print(json_loaded)
      if json_loaded["class"] == "TPV":
        gps_data = json_loaded["class"=="TPV"]
        return gps_data
    print("No objects found")
    return gps_data



print(gps())