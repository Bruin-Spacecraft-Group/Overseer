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
from gpiozero import LED
from time import sleep
print("Running main.py")

# 1. CPU Health

# 1. CPU Health - print temp, clock, volt, top


def cpu():
    cpu = CPUTemperature()

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

    out = "Temp: " + str(cpu.temperature) + "ºC\n"

    clock = round(int(clockOutput) / 1000000000.0, 2)
    out += "Clock: " + str(clock) + "GHz\n"
    out += "Voltage: " + str(voltsOutput)[:-1] + "V\n"

    usage = round(100 - float(cpuUsage[cpuUsers.index("%idle")]), 2)
    out += "Usage: " + str(usage) + "%\n"

    print(out)
    return out

# 2. Camera - take a picture


def camera():
    camera = PiCamera()
    # record 5 seconds
    # camera.start_preview()
    # camera.start_recording('video.h264')
    # camera.wait_recording(5)
    # camera.stop_recording()
    # camera.stop_preview()

    # take a picture
    fname = datetime.now().strftime("%H-%M-%S") + ".jpg"
    camera.start_preview()
    camera.capture(fname)
    camera.stop_preview()
    out = "pic: " + fname + "\n"
    print(out)
    return out

# 3. MPU6050 - print accel, gyro, temp


def mpu6050():
    i2c = board.I2C()  # defaults 0x68
    mpu = adafruit_mpu6050.MPU6050(i2c)

    temp_offset = -8

    # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    out = "Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2\n" % (mpu.acceleration)
    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    out += "Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s\n" % (mpu.gyro)
    # print("Temperature (MPU): %.2f C" % (mpu.temperature + temp_offset))
    out += "Temperature (MPU): %.2f C\n" % (mpu.temperature + temp_offset)

    print(out)
    return out


# 4. BME280 - print temp, pressure, humidity
def bme280():
    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # defualts 0x77
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

    # change this to match the location's pressure (hPa) at sea level
    bme680.sea_level_pressure = 1014.22

    temperature = bme680.temperature
    gas = bme680.gas
    relative_humidity = bme680.relative_humidity
    pressure = bme680.pressure
    altitude = bme680.altitude

    temp_offset = -6.5
    # print("Temperature (BME): %0.1f C" % (bme680.temperature + temp_offset))
    # print("Gas Resistance: %d ohm" % bme680.gas)
    # print("Relative Humidity: %0.1f %%" % bme680.relative_humidity)
    # print("Pressure: %0.3f hPa" % bme680.pressure)
    # print("Altitude = %0.2f meters" % bme680.altitude)
    out = "Temperature (BME): %0.1f C\n" % (bme680.temperature + temp_offset)
    out += "Gas Resistance: %d ohm\n" % bme680.gas
    out += "Relative Humidity: %0.1f %%\n" % bme680.relative_humidity
    out += "Pressure: %0.3f hPa\n" % bme680.pressure
    out += "Altitude = %0.2f meters\n" % bme680.altitude

    print(out)
    return out

# 5. GPS - print lat, lon, alt, speed, climb, eps, epc


def gps():
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
    print(out)
    return out

# Cutdown function


def cutdown():
    pin = LED(16)
    it = time.time()
    while it != 5:
        it = time.time()
        pin.on()
        sleep(1)  # TODO REMOVE
        pin.off()
        sleep(1)  # TODO REMOVE
        print(it)


# Try each function

# 1. CPU - print temp, clock, voltage, usage
try:
    with open("flight_log.txt", "a+") as f:
        f.write(cpu())
        f.close()
except Exception as e:
    print("CPU Error:", e)


# 2. Camera - take a picture
try:
    with open("flight_log.txt", "a+") as f:
        f.write(camera())
        f.close()
except Exception as e:
    print("Camera Error:", e)


# 3. MPU6050 - print accel, gyro, temp
try:
    with open("flight_log.txt", "a+") as f:
        f.write(mpu6050())
        f.close()
except Exception as e:
    print("MPU Error:", e)

# 4. BME280 - print temp, pressure, humidity
try:
    with open("flight_log.txt", "a+") as f:
        f.write(bme280())
        f.close()
except Exception as e:
    print("BME Error:", e)

# 5. GPS - print lat, lon, alt, speed, climb, eps, epc
try:
    with open("flight_log.txt", "a+") as f:
        f.write(gps())
        f.close()
except Exception as e:
    print("GPS Error:", e)

# end mesage
finally:
    print("Finished main.py")

# TODO: 6. Relay - turn on and off
# try:
#     with open("flight_log.txt", "a+") as f:
#         f.write(gps())
# except:
#     print("GPS Error")
