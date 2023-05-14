
import time
from main import camera, cutdown

def checkOutputFile():
    file = open("~/FLIGHT_DATA_S23/flight_output.txt", "r")
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
        except:
            print("Cutdown Error")

    if "picture" in lastTenLinesString:
        print("Taking Picture")
        
        try:
            with open("flight_log.txt", "a+") as f:
                f.write(camera())
        except:
            print("Camera Error")



while True:
    checkOutputFile()
    time.sleep(5)