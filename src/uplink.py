
import time
import os

from picamera import PiCamera
from datetime import datetime

from gpiozero import LED
GPIO_PIN = 27

# Camera - take a picture

# WE DONT USE THIS ANYMORE - because we can only have 1 instance at a time and race condition is bad with main
def camera():
    camera = PiCamera()
    camera.resolution = (1920, 1080)

    cwd = os.getcwd()
    os.chdir("/home/overseer/FLIGHT_DATA_S23/PICTURES")
    fname = datetime.now().strftime("%H:%M:%S") + ".h264"

    camera.start_preview()
    camera.start_recording(fname)
    camera.wait_recording(5)
    camera.stop_recording()
    camera.stop_preview()

    os.chdir(cwd)
    
    return fname

# TODO: Cutdown function w/ nichrome test


def cutdown():
    print("Cutdown activated")
    pin = LED(GPIO_PIN)
    pin.on()
    time.sleep(4)
    pin.off()
    sleep(2)
    pin.on()
    sleep(4)
    pin.off()


monitor_file_path = "~/FLIGHT_DATA_S23/flight_output.txt"


def checkOutputFile():
    file = open(os.path.expanduser(monitor_file_path), "r")
    fileContent = file.readlines()
    file.close()

    lastTenLines = fileContent[-10:]
    lastTenLinesString = "\n".join(lastTenLines)

    # IMPORTANT: choose string
    searchString = "cutdownOverseer"

    if searchString in lastTenLinesString:
        print("Activating Cutdown")

        try:
            with open("flight_log.txt", "a+") as subfile:
                subfile.write(cutdown())
            subfile.close()
        except:
            print("Cutdown Error")

    searchString = "activateVideo"

    if searchString in lastTenLinesString:
        print("Taking Video")

        try:
            with open("flight_log.txt", "a+") as subfile:
                subfile.write(camera())
            subfile.close()
        except:
            print("Video Error")


while True:
    try:
        checkOutputFile()
    except:
        print("Error checking uplink")
    time.sleep(5)
