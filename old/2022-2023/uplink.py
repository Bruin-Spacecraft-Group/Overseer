
import time
import os

from gpiozero import LED
GPIO_PIN = 27

# TODO: Cutdown function w/ nichrome test

def cutdown():
    print("Cutdown activated")
    pin = LED(GPIO_PIN)
    pin.on()
    time.sleep(4)
    pin.off()
    time.sleep(2)
    pin.on()
    time.sleep(4)
    pin.off()


monitor_file_path = "~/FLIGHT_DATA_S23/flight_output.txt"

def checkOutputFile():
    file = open(os.path.expanduser(monitor_file_path), "r")
    fileContent = file.readlines()
    file.close()

    lastNLines = fileContent[-5:]
    lastNLinesString = "\n".join(lastNLines)

    # IMPORTANT: choose string
    searchString = "cutdownOverseer"

    if searchString in lastNLinesString:
        print("Activating Cutdown")
        try:
            cutdown()
        except:
            print("Error activating cutdown")


while True:
    try:
        checkOutputFile()
    except:
        print("Error checking uplink")
    time.sleep(5)
