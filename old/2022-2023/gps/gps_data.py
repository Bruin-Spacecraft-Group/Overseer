import json
import subprocess

'''
Runs gpspipe which outputs json objects.
Parses json and saves data we want to a dictionary

Notes:
Number of runs=5 because in testing we found this is when the data first comes in.
Might need to change this based on the output after the first 5 runs
'''

def gps_data():

    # TODO: Test on pi to ensure file creation and piping works properly.

    f = open("gps_data.json", "w") # create file
    subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f) # run and pipe to file
    f = open("gps_data.json", "r") # read file
    gps_data = dict()
    for line in f:
        json_loaded = json.loads(line)
        if json_loaded["class"] == "TPV": # only get TPV object
            gps_data = parse_json(json_loaded)
            return gps_data

    print("No objects found")
    return gps_data
          

def parse_json(json_data):
    keywords = ["lat", "lon", "altHAE", "epx", "epy", "epv", "speed", "climb", "eps", "epc"] # keywords we want
    data_dict = dict()
    for keyword in keywords:
        data_dict[keyword] = json_data[keyword] # save data we want to a dictionary
    return data_dict


def main():
    print(gps_data())

if __name__ == "__main__":
    main()