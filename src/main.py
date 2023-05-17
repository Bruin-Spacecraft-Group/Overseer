# main

from decimal import Decimal
import subprocess
import json
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
        self.f = fname
        self.cpu = CPUTemperature()
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)
        self.i2c = board.I2C()  # MPU defaults 0x68, BME defaults 0x77
        self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
        # change this to match the location's pressure (hPa) at sea level
        self.bme680.sea_level_pressure = 1014.22
        self._MPU_TEMP_OFFSET = -8
        self._BME_TEMP_OFFSET = -6.5
        

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

        clock = round(int(clockOutput) / 1000000000.0, 2)
        usage = round(100 - float(cpuUsage[cpuUsers.index("%idle")]), 2)

        # out = "Temp: " + str(cpu.temperature) + "ºC\n"
        # out += "Clock: " + str(clock) + "GHz\n"
        # out += "Voltage: " + str(voltsOutput)[:-1] + "V\n"
        # out += "Usage: " + str(usage) + "%\n"

        # TODO: remove redundancy
        print_out = "CPU," + str(self.cpu.temperature) + "ºC" + "," + str(clock) + "GHz" + "," + \
            str(voltsOutput)[:-1] + "V"+"," + str(usage) + "%"
        json_out = "CPU:{\"temp\":" + str(self.cpu.temperature) + \
            ",\"clock\":" + str(clock) + ",\"volt\":" + \
            str(voltsOutput)[:-1] + ",\"usage\":" + str(usage) + "}"
        return print_out, json_out

    # 2. Camera - take a picture; returns json_out
    def __camera(self):
        cwd = os.getcwd()
        os.chdir("/home/overseer/FLIGHT_DATA_S23/PICTURES")
        fname = datetime.now().strftime("%H:%M:%S") + ".jpg"
        self.camera.start_preview()
        self.camera.capture(fname)
        self.camera.stop_preview()
        os.chdir(cwd)
        json_out = "pic: " + fname
        return json_out

    # 3. MPU6050 - print accel, gyro, temp; returns print_out, json_out
    def __mpu6050(self):
        accel = self.mpu.acceleration
        gyro = self.mpu.gyro
        temp = self.mpu.temperature + self._MPU_TEMP_OFFSET
        out = "Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2\n" % accel
        out += "Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s\n" % gyro
        out += "Temperature (MPU): %.2f C\n" % temp
        print_out = out
        json_out = "MPU6050:{\"accel\":[" + str(accel[0]) + "," + str(accel[1]) + "," + str(accel[2]) + "],\"gyro\":[" + str(gyro[0]) + "," + str(gyro[1]) + "," + str(gyro[2]) + "],\"temp\":" + str(temp) + "}"
        return print_out, json_out

    # 4. BME280 - print temp, pressure, humidity
    def __bme280(self):
        temperature = self.bme680.temperature + self._BME_TEMP_OFFSET
        gas = self.bme680.gas
        relative_humidity = self.bme680.relative_humidity
        pressure = self.bme680.pressure
        altitude = self.bme680.altitude
        out = "Temperature (BME): %0.1f C\n" % temperature
        out += "Gas Resistance: %d ohm\n" % gas
        out += "Relative Humidity: %0.1f %%\n" % relative_humidity
        out += "Pressure: %0.3f hPa\n" % pressure
        out += "Altitude (BME) = %0.2f meters\n" % altitude
        print_out = out
        json_out = "BME280:{\"temp\":" + str(temperature) + ",\"gas\":" + str(gas) + ",\"humidity\":" + str(relative_humidity) + ",\"pressure\":" + str(pressure) + ",\"altitude\":" + str(altitude) + "}"
        return print_out, json_out

    # 5. GPS - print lat, lon, alt, speed, climb, eps, epc
    def __gps(self):
        def gps_data():
            f = open("gps_data.json", "w")  # create file
            subprocess.run(["gpspipe", "-w", "-n", "5"],
                           stdout=f)  # run and pipe to file
            f = open("gps_data.json", "r")  # read file
            gps_data = dict()
            for line in f:
                json_loaded = json.loads(line)
                if json_loaded["class"] == "TPV":  # only get TPV object
                    gps_data = parse_json(json_loaded)
                    return gps_data
            print("No objects found")
            return gps_data

        def parse_json(json_data):
            keywords = ["lat", "lon", "altHAE", "epx", "epy", "epv",
                        "speed", "climb", "eps", "epc"]  # keywords we want
            data_dict = dict()
            for keyword in keywords:
                # save data we want to a dictionary
                data_dict[keyword] = json_data[keyword]
            return data_dict
        out = gps_data()
        return out

    def run(self):
        # 1. CPU - print temp, clock, voltage, usage
        try:
            cpu_out = self.__cpu()
        except Exception as e:
            cpu_out = "CPU error: " + str(e)
        # 2. Camera - take a picture
        try:
            camera_out = self.__camera()
        except Exception as e:
            camera_out = "Camera error: " + str(e)
        # 3. MPU6050 - print accel, gyro, temp
        try:
            mpu_out = self.__mpu6050()
        except Exception as e:
            mpu_out = "MPU6050 error: " + str(e)
        # 4. BME280 - print temp, pressure, humidity
        try:
            bme_out = self.__bme280()
        except Exception as e:
            bme_out = "BME280 error: " + str(e)
        # 5. GPS - print lat, lon, alt, speed, climb, eps, epc
        try:
            gps_out = self.__gps()
        except Exception as e:
            gps_out = "GPS error: " + str(e)
        # 6. Write to file
        with open(self.f, "a+") as f:
            f.write(cpu_out[0] + "\n")
            f.write(camera_out + "\n")
            f.write(mpu_out[0] + "\n")
            f.write(bme_out[0] + "\n")
            f.write(gps_out + "\n")
            f.write("\n")
            f.close()
        # 7. Print to console
        print(cpu_out[0])
        print(camera_out)
        print(mpu_out[0])
        print(bme_out[0])
        print(gps_out)


# Try each function

def main():
    fcu = FlightControlUnit("test_log.txt")
    fcu.run()
    # # 1. CPU - print temp, clock, voltage, usage
    # try:
    #     with open("flight_log.txt", "a+") as f:
    #         f.write(cpu())
    #         f.close()
    # except Exception as e:
    #     print("CPU Error:", e)
    # # 2. Camera - take a picture
    # try:
    #     with open("flight_log.txt", "a+") as f:
    #         f.write(camera())
    #         f.close()
    # except Exception as e:
    #     print("Camera Error:", e)
    # # 3. MPU6050 - print accel, gyro, temp
    # try:
    #     with open("flight_log.txt", "a+") as f:
    #         f.write(mpu6050())
    #         f.close()
    # except Exception as e:
    #     print("MPU Error:", e)
    # # 4. BME280 - print temp, pressure, humidity
    # try:
    #     with open("flight_log.txt", "a+") as f:
    #         f.write(bme280())
    #         f.close()
    # except Exception as e:
    #     print("BME Error:", e)
    # # 5. GPS - print lat, lon, alt, speed, climb, eps, epc
    # try:
    #     with open("flight_log.txt", "a+") as f:
    #         f.write(gps())
    #         f.close()
    # except Exception as e:
    #     print("GPS Error:", e)
    # finally:
    #     print("Done")

if __name__ == "__main__":
    main()
