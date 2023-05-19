
import json, subprocess

# capture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]

def gps():
  with open("gps_data.json", "w") as f:
    subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
  with open("gps_data.json", "r") as f:
    gps_data = []
    for line in f:
      json_loaded = json.loads(line)
      if json_loaded["class"] == "TPV":
        if json_loaded["lat"]:
          gps_data.append(json_loaded["lat"])
        if json_loaded["lon"]:
          gps_data.append(json_loaded["lon"])
        if json_loaded["altHAE"]:
          gps_data.append(json_loaded["altHAE"])
        if json_loaded["epx"]:
          gps_data.append(json_loaded["epx"])
        if json_loaded["epy"]:
          gps_data.append(json_loaded["epy"])
        if json_loaded["epv"]:
          gps_data.append(json_loaded["epv"])
        if json_loaded["speed"]:
          gps_data.append(json_loaded["speed"])
        if json_loaded["climb"]:
          gps_data.append(json_loaded["climb"])
        if json_loaded["eps"]:
          gps_data.append(json_loaded["eps"])
        if json_loaded["epc"]:
          gps_data.append(json_loaded["epc"])
        return gps_data



print(gps())