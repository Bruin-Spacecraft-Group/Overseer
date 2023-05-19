
import json, subprocess

def parse_json(json_data):
  # caapture values of keys ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]
  keywords = ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"]
  data_dict = dict()
  for keyword in keywords:
    data_dict[keyword] = json_data[keyword]
  return data_dict



def gps():
    with open("gps_data.json", "w") as f:
        subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
    with open("gps_data.json", "r") as f:
        gps_data = dict()
        for line in f:
            json_loaded = json.loads(line)
            if json_loaded["class"] == "TPV":
                gps_data = parse_json(json_loaded)
                return gps_data
        print("No objects found")
        return gps_data


print(gps())