# main


# 1. CPU Health
from time import sleep
from gpiozero import LED
import adafruit_bme680
import time
import adafruit_mpu6050
import board
from datetime import datetime
from picamera import PiCamera
from gpiozero import CPUTemperature
import json
import subprocess
from decimal import Decimal

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

    # usageObject = {}
    # usageObject["idle"] = cpuUsage[cpuUsers.index("%idle")]

    # usageObjectJson = json.dumps(usageObject)

    # create json object
    # outputObject = {
    #     "t": str(cpu.temperature),
    #     "c": str(clockOutput),
    #     "v": str(voltsOutput),
    #     "cpu": str(usageObjectJson),
    # }

    print("Temp:", cpu.temperature, "ºC")

    clock = round(int(clockOutput) / 1000000000.0, 2)
    print("Clock:", clock, "GHz")

    print("Voltage:", str(voltsOutput)[:-1], "V")

    usage = round(100 - float(cpuUsage[cpuUsers.index("%idle")]), 2)
    print("Usage:", usage, "%")

    # output json object
    # outputJSON = json.dumps(outputObject)
    # print(outputJSON)


# 2. Camera - take a picture
def camera():
    try:
        camera = PiCamera()
    except:
        print("Camera not connected")
        return

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

# 3. MPU6050 - print accel, gyro, temp


def mpu6050():
    i2c = board.I2C()  # defaults 0x68
    mpu = adafruit_mpu6050.MPU6050(i2c)

    temp_offset = -8

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    print("Temperature (MPU): %.2f C" % (mpu.temperature + temp_offset))


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
    print("Temperature (BME): %0.1f C" % (bme680.temperature + temp_offset))
    print("Gas Resistance: %d ohm" % bme680.gas)
    print("Relative Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

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
    print(gps_data())


def relay():
    pin = LED(16)
    it = time.time()
    while it != 5:
        it = time.time()
        pin.on()
        sleep(1)
        pin.off()
        sleep(1)
        print(it)


# time.sleep(2)
# try each function
try:
    cpu()
except:
    print("CPU Error")
try:
    relay()
except:
    print("Relay Error")
try:
    camera()
except:
    print("Camera Error")
    mpu6050()
try:
    bme280()
except:
    print("BME280 Error")
try:
    gps()
except:
    print("GPS Error")
