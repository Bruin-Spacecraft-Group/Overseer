# main
from decimal import Decimal
import subprocess
from json import loads
from gpiozero import CPUTemperature
from picamera import PiCamera
from datetime import datetime
import board
import adafruit_mpu6050
import time
import adafruit_bme680
from time import sleep
import os

from cam import cam_test

class FlightControlUnit:

    def __init__(self, fname):
        self.initStatus = True
        self.f = fname

        self.camera = cam_test.MyCamera()

    # 1. Camera - take a video; return json out
    def __camera(self):
        cwd = os.getcwd()
        os.chdir("/home/overseer/FLIGHT_DATA_S24/PICTURES")
        vid_fname = datetime.now().strftime("%H-%M-%S") + ".h264"
        pic_fname = datetime.now().strftime("%H:%M:%S") + ".jpg"
        self.camera.record_video(vid_fname, pic_fname, altitude=100,reached_threshold=False) #TODO: change so not hardcoded
        os.chdir(cwd)
        return vid_fname
    # TODO: insert other modules

    def run(self):
        # 1. Camera - take a video/picture
        try:
            camera_out = self.__camera()
        except:
            camera_out = "e"
        #TODO: insert other modules
        
        # Write to file
        print_out = camera_out + "\n"
        write_out = datetime.now().strftime("%H:%M:%S") + "," + print_out
        with open(self.f+"_1.csv", "a+") as f:
            f.write(write_out)

        # Print to console
        print(print_out)


def main():
    # DO NOT ENTER FILE EXTENSION - only the name you want the base file to be, we save as .csv
    fcu = FlightControlUnit(
        "/home/overseer/FLIGHT_DATA_S24/DATA/flight_log")
    
    while True:
        fcu.run()
        time.sleep(30)


if __name__ == "__main__":
    main()
