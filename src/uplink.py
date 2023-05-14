
import time
from main import camera, cutdown

import os

monitor_file_path = "~/FLIGHT_DATA_S23/flight_output.txt"

def checkOutputFile():
    file = open(os.path.expanduser(monitor_file_path), "r")
    fileContent = file.read()
    file.close()

    splitFileContent = fileContent.split("\n")
    lastTenLines = splitFileContent[-10:]
    lastTenLinesString = "\n".join(lastTenLines)

    if "cutdown" in lastTenLinesString:
        print("Activating Cutdown")

        try:
            with open("flight_log.txt", "a+") as f:
                f.write(cutdown())
            f.close()
        except:
            print("Cutdown Error")

    if "picture" in lastTenLinesString:
        print("Taking Picture")
        
        try:
            with open("flight_log.txt", "a+") as f:
                f.write(camera())
            f.close()
        except:
            print("Camera Error")



while True:
    try:
        checkOutputFile()
    except:
        print("Error checking uplink")
    time.sleep(5)