# main
from decimal import Decimal
import subprocess
from json import loads
import json
#from gpiozero import CPUTemperature
from datetime import datetime
#import board
#import adafruit_mpu6050
import time
#import adafruit_bme680
from time import sleep
import os
import argparse

from cam import cam_test
from cpu_health import metrics
from accelerometer import MPU_6050
from temp_press import Temp_Press
from gps_v2 import gps
from relay import relay

#TODO: accelerometer and temp/pres don't work currently (i2c error)
#      have it instead hard coded to a cutdown time

class FlightControlUnit:

    def __init__(self, fname):
        self.init_status = True
        self.launch_threshold = False
        self.prev_launch_threshold = False
        self.cutdown_threshold = False
        self.prev_cutdown_threshold = False
        self.f = fname

        self.start_time = datetime.now()

        self.cpu = metrics.CPUMetrics()
        self.camera = cam_test.MyCamera()
#        self.accelerometer = MPU_6050.accelerometer()
#        self.temp = Temp_Press.TempPress()
        self.gps = gps.myGPS()
        self.relay = relay.Relay()

    # 1. CPU - returns cpu health data as json
    def __cpu_health(self):
        cpu_metrics = self.cpu.get_metrics()
        return json.dumps(cpu_metrics)

    # 2. Camera - take a video; return json out
    def __camera(self):
        cwd = os.getcwd()
        os.chdir("/home/overseer4/FLIGHT_DATA_S24/PICTURES")
        vid_fname = datetime.now().strftime("%H-%M-%S") + ".h264"
        pic_fname = datetime.now().strftime("%H:%M:%S") + ".jpg"
        should_record = self.launch_threshold or self.cutdown_threshold
        cam_files = self.camera.record_video(vid_fname, pic_fname, should_record)
        os.chdir(cwd)

        return json.dumps(cam_files)
    
    # 3. Accelerometer - gives accelerometer data
    def __accelerometer(self):
        accelerometer_data = self.accelerometer.mpu_data()
        return json.dumps(accelerometer_data)

    # 4. Temp_Press - gives temp/pressure data
    def __temp(self):
        temp_pres_data = self.temp.record_tp()
        return json.dumps(temp_pres_data)

    # 5. GPS - gives positional data
    def __gps(self):
        try:
            gps_data = self.gps.get_gps_data()
            json_out = gps_data

            #TODO: check initial altitude thresholds and pressure thresholds
            #set launch threshold after 60 seconds
            if (int((datetime.now() - self.start_time).total_seconds())) > 20 and not self.prev_launch_threshold:
                self.launch_threshold = True
                self.prev_launch_threshold = True
            else:
                self.launch_threshold = False

            #set cutdown threshold after 2 hours
            if (int((datetime.now() - self.start_time).total_seconds())) > 7200 and not self.prev_cutdown_threshold:
                self.cutdown_threshold = True
                self.prev_cutdown_threshold = True
            else:
                self.cutdown_threshold = False

            """
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
            """

            # sets return string
            rets = []
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
            return str(rets)
        except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly
            self.gps.stop()
        except Exception as x:
            print(x)
            raise x
        
    # 6. Relay - cuts down payload if reached altitude threshold
    def __relay(self):
        relay_data = self.relay.cutdown(self.cutdown_threshold)
        return json.dumps(relay_data)


    def run(self):
        # 0. Time since launch
        try:
            time_since_launch = {
                "start_time": str(self.start_time),
                "curr_time": str(datetime.now()),
                "time_since_launch": int((datetime.now() - self.start_time).total_seconds())
            }
            time_out = json.dumps(time_since_launch)
        except Exception as e:
            time_out = "e"

        #1. CPU - cpu health data
        try:
            cpu_out = self.__cpu_health()
        except:
            cpu_out = "e"

        #2. Camera - take a video/picture
        try:
            camera_out = self.__camera()
        except Exception as x:
            print(x)
            camera_out = "e"

        """
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
        """

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
        print_out = time_out + "," + cpu_out + "," + camera_out + "," + gps_out + ',' + relay_out + '\n'
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
    parser = argparse.ArgumentParser(description='Flight Control Unit')
    parser.add_argument('-t', '--test', action='store_true', help='Use the test directory for the flight log file')
    args = parser.parse_args()

    # DO NOT ENTER FILE EXTENSION - only the name you want the base file to be, we save as .csv
    log_directory = "/home/overseer4/FLIGHT_DATA_S24/TEST" if args.test else "/home/overseer4/FLIGHT_DATA_S24/DATA"
    log_filename = "flight_log"
    log_path = os.path.join(log_directory, log_filename)

    fcu = FlightControlUnit(log_path)
    
    while True:
        fcu.run()
        time.sleep(30)

if __name__ == "__main__":
    main()
