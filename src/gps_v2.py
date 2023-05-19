
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
        try:
          gps_data.append(json_loaded["lat"])
        except:
          pass
        try:
          gps_data.append(json_loaded["lon"])
        except:
          pass
        try:
          gps_data.append(json_loaded["altHAE"])
        try:
          gps_data.append(json_loaded["epx"])
        except:
          pass
        try:
          gps_data.append(json_loaded["epy"])
        except:
          pass
        try:
          gps_data.append(json_loaded["epv"])
        except:
          pass
        try:
          gps_data.append(json_loaded["speed"])
        except:
          pass
        try:
          gps_data.append(json_loaded["climb"])
        except:
          pass
        try:
          gps_data.append(json_loaded["eps"])
        except:
          pass
        try:
          gps_data.append(json_loaded["epc"])
        except:
          pass
        return gps_data



print(gps())