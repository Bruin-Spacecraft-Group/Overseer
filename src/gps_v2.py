
import json, subprocess

# capture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]

def gps():
  with open("gps_data.json", "w") as f:
    subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
  with open("gps_data.json", "r") as f:
    gps_data = list()
    for line in f:
      json_loaded = json.loads(line)
      if json_loaded["class"] == "TPV":
        gps_data = list(json_loaded["lat"], json_loaded["lon"], json_loaded["altHAE"], json_loaded["epx"], json_loaded["epy"], json_loaded["epv"], json_loaded["speed"], json_loaded["climb"], json_loaded["eps"], json_loaded["epc"])
        return gps_data



print(gps())