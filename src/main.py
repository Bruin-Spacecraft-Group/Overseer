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

# 1. CPU Health - print temp, clock, volt, top


class FlightControlUnit:

    def __init__(self, fname):
        self.initStatus = True
        self.f = fname

        self._MPU_TEMP_OFFSET = -8
        self._BME_TEMP_OFFSET = -6.5
        try:
            self.cpu = CPUTemperature()
        except:
            pass
        try:
            self.camera = PiCamera()
        except:
            pass
        try:
            self.camera.resolution = (1920, 1080)
        except:
            pass
        try:
            self.i2c = board.I2C()  # MPU defaults 0x68, BME defaults 0x77
        except:
            pass
        try:
            self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
        except:
            pass
        try:
            self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
            # change this to match the location's pressure (hPa) at sea level
            self.bme680.sea_level_pressure = 1014.22
        except:
            pass

    # 1. CPU Health - print temp, clock, volt, top; returns print_out, json_out

    def __cpu(self):
        clockOutput = subprocess.check_output(
            ['vcgencmd', 'measure_clock', 'arm']).decode()[:-1]  # clock
        clockOutput = clockOutput[clockOutput.index("=") + 1:]
        voltsOutput = subprocess.check_output(
            ['vcgencmd', 'measure_volts', 'core']).decode()[:-1]  # cpu voltage
        voltsOutput = voltsOutput[voltsOutput.index("=") + 1:]
        mpstatOutput = subprocess.check_output(['mpstat'])  # cpu usage

        mpstatLines = mpstatOutput.splitlines()
        cpuUsers = mpstatLines[2].split()
        cpuUsers = [x.decode() for x in cpuUsers]
        cpuUsage = mpstatLines[3].split()
        cpuUsage = [x.decode() for x in cpuUsage]

        temp = self.cpu.temperature
        clock = round(int(clockOutput) / 1000000000.0, 2)
        usage = round(100 - float(cpuUsage[cpuUsers.index("%idle")]), 2)
        # TODO: fix rounding
        out = str(round(temp, 2)) + "," + str(round(clock, 2)) + \
            "," + str(voltsOutput)[:4] + "," + str(round(usage, 2))
        return out

    # 2. Camera - take a picture; returns json_out
    def __camera(self):
        cwd = os.getcwd()
        os.chdir("/home/overseer/FLIGHT_DATA_S23/PICTURES")
        fname = datetime.now().strftime("%H:%M:%S") + ".jpg"
        self.camera.start_preview()
        self.camera.capture(fname)
        self.camera.stop_preview()
        os.chdir(cwd)
        return fname

    # 3. MPU6050 - print accel, gyro, temp; returns print_out, json_out
    def __mpu6050(self):
        accel = self.mpu.acceleration
        gyro = self.mpu.gyro
        temp = self.mpu.temperature + self._MPU_TEMP_OFFSET
        out = str(round(accel[0], 2)) + "," + str(round(accel[1], 2)) + "," + str(round(accel[2], 2)) + "," + str(
            round(gyro[0], 2)) + "," + str(round(gyro[1], 2)) + "," + str(round(gyro[2], 2)) + "," + str(round(temp, 2))
        return out

    # 4. BME280 - print temp, pressure, humidity
    def __bme280(self):
        temperature = self.bme680.temperature + self._BME_TEMP_OFFSET
        gas = self.bme680.gas / 1000
        relative_humidity = self.bme680.relative_humidity
        pressure = self.bme680.pressure
        altitude = self.bme680.altitude
        out = str(round(temperature, 2)) + "," + str(round(gas, 2)) + "," + str(round(
            relative_humidity, 2)) + "," + str(round(pressure, 2)) + "," + str(round(altitude, 2))
        return out

    # 5. GPS - print lat, lon, alt, speed, climb, eps, epc
    def __gps(self):
        rets = []
        json_out = {}
        with open("gps_data.json", "w") as f:
            subprocess.run(["gpspipe", "-w", "-n", "5"], stdout=f)
        with open("gps_data.json", "r") as f:
            gps_data = []
            for line in f:
                json_loaded = loads(line)
                if json_loaded["class"] == "TPV":
                    json_out = json_loaded
                    break
        try:
            rets.append(str(round(json_out["lat"],4)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["lon"],4)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["altHAE"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["epx"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["epy"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["epv"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["speed"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["climb"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["eps"],2)))
        except:
            rets.append("e")
        try:
            rets.append(str(round(json_out["epc"],2)))
        except:
            rets.append("e")
        return rets



    def run(self):
        # 1. CPU - print temp, clock, voltage, usage
        try:
            cpu_out = self.__cpu()
        except:
            cpu_out = "e,e,e,e"
        # 2. Camera - take a picture
        try:
            camera_out = self.__camera()
        except:
            camera_out = "e"
        # 3. MPU6050 - print accel, gyro, temp
        try:
            mpu_out = self.__mpu6050()
        except:
            mpu_out = "e,e,e,e,e,e,e"
        # 4. BME280 - print temp, pressure, humidity
        try:
            bme_out = self.__bme280()
        except:
            bme_out = "e,e,e,e,e"
        # 5. GPS - print lat, lon, alt, speed, climb, eps, epc
        try:
            gps_out = self.__gps()
        except:
            gps_out = {"1": "e", "2": "e", "3": "e", "4": "e", "5": "e", "6": "e", "7": "e", "8": "e", "9": "e", "10": "e"}
        # 6. Write to file
        print_out = cpu_out + "," + camera_out + "," + mpu_out + "," + bme_out + "," + ",".join(gps_out) + "\n"
        write_out = datetime.now().strftime("%H:%M:%S") + "," + print_out
        with open(self.f+"_1.csv", "a+") as f:
            f.write(write_out)
        with open(self.f+"_2"+".csv", "a+") as f:
            f.write(write_out)
        with open(self.f+"_3"+".csv", "a+") as f:
            f.write(write_out)
        # 7. Print to console
        print(print_out)


# Try each function

def main():
    # DO NOT ENTER FILE EXTENSION - only the naame you want the base file to be, we save as .csv
    fcu = FlightControlUnit(
        "/home/overseer/FLIGHT_DATA_S23/DATA/flight_log")
    fcu.run()


if __name__ == "__main__":
    main()
