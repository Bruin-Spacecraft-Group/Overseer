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
from cpu_health import metrics
from accelerometer import MPU_6050
from temp_press import Temp_Press
from gps import gps
from relay import relay


#TODO: edit add cutdown, reached_threshold so not hardcoded, fix camera output
#TODO: see if can just say e for all if failure (may need more)
#TODO: check json
#TODO: see if while loop is valid

class FlightControlUnit:

    def __init__(self, fname):
        self.init_status = True
        self.launch_threshold = False
        self.prev_launch_threshold = False
        self.cutdown_threshold = False
        self.prev_cutdown_threshold = False
        self.f = fname

        self.cpu = metrics.CPUMetrics()
        self.camera = cam_test.MyCamera()
        self.accelerometer = MPU_6050.accelerometer()
        self.temp = Temp_Press.TempPress()
        self.gps = gps.Ublox()
        self.relay = relay.Relay()

        self.gps.start()

    # 1. CPU - returns cpu health data as json
    def __cpu_health(self):
        return self.cpu.get_metrics()

    # 2. Camera - take a video; return json out
    def __camera(self):
        cwd = os.getcwd()
        os.chdir("/home/overseer/FLIGHT_DATA_S24/PICTURES")
        vid_fname = datetime.now().strftime("%H-%M-%S") + ".h264"
        pic_fname = datetime.now().strftime("%H:%M:%S") + ".jpg"
        should_record = self.launch_threshold or self.cutdown_threshold
        self.camera.record_video(vid_fname, pic_fname, should_record)
        os.chdir(cwd)
        return vid_fname
    
    # 3. Accelerometer - gives accelerometer data
    def __accelerometer(self):
        return self.accelerometer.mpu_data()

    # 4. Temp_Press - gives temp/pressure data
    def __temp(self):
        return self.temp.record_tp()

    # 5. GPS - gives positional data
    def __gps(self):
        try:
            gps_data = gps.get_data()

            #TODO: check initial altitude thresholds and pressure thresholds

            # sets launch threshold to true the first time we hit 100m (to record a video)
            if gps_data["alt"] > 100 and not self.prev_launch_threshold:
                self.launch_threshold = True
                self.prev_launch_threshold = True
            else:
                self.launch_threshold = False

            if gps_data["alt"] > 100000 and not self.prev_cutdown_threshold:
                self.cutdown_threshold = True
                self.prev_cutdown_threshold = True
            else:
                self.cutdown_threshold = False

            return gps_data
        except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly
            gps.stop()
        except Exception as x:
            raise x
        
    # 6. Relay - cuts down payload if reached altitude threshold
    def __relay(self):
        return self.relay.cutdown(self.cutdown_threshold)


    def run(self):
        #1. CPU - cpu health data
        try:
            cpu_out = self.__cpu_health()
        except:
            cpu_out = "e"

        #2. Camera - take a video/picture
        try:
            camera_out = self.__camera()
        except:
            camera_out = "e"
        
        #3. accelerometer
        try:
            accelerometer_out = self.__accelerometer()
        except:
            accelerometer_out = "e"

        #4. temp_press
        try:
            temp_out = self.__temp()
        except:
            temp_out = "e"

        #5. GPS
        try:
            gps_out = self.__gps()
        except:
            gps_out = "e"

        #6. Relay
        try:
            relay_out = self.__relay()
        except:
            relay_out = "e"
        
        #F. Write to file (write to multiple for redundance)
        print_out = cpu_out + "," + camera_out + "," + accelerometer_out + "," + temp_out + "," + gps_out + ',' + relay_out + '\n'
        write_out = datetime.now().strftime("%H:%M:%S") + "," + print_out
        with open(self.f+"_1.csv", "a+") as f:
            f.write(write_out)
        with open(self.f+"_2.csv", "a+") as f:
            f.write(write_out)
        with open(self.f+"_3.csv", "a+") as f:
            f.write(write_out)
        with open(self.f+"_4.csv", "a+") as f:
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
