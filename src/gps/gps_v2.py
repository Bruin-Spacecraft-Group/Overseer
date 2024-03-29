
from subprocess import run
from json import loads

# capture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]

def gps():
  rets = []
  json_out = {}
  with open("gps_data.json", "w") as f:
    run(["gpspipe", "-w", "-n", "5"], stdout=f)
  with open("gps_data.json", "r") as f:
    gps_data = []
    for line in f:
      json_loaded = loads(line)
      if json_loaded["class"] == "TPV":
        json_out = json_loaded
        break
  try:
    rets.append(json_out["lat"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["lon"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["altHAE"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["epx"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["epy"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["epv"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["speed"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["climb"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["eps"])
  except:
    rets.append("e")
  try:
    rets.append(json_out["epc"])
  except:
    rets.append("e")
  return rets


print(gps())