# main


# 1. CPU Health
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

def get_cpu_temp():
    cpu = CPUTemperature()

    clockOutput = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode()[:-1] # clock
    clockOutput = clockOutput[clockOutput.index("=") + 1:]
    voltsOutput = subprocess.check_output(['vcgencmd', 'measure_volts', 'core']).decode()[:-1] # cpu voltage
    voltsOutput = voltsOutput[voltsOutput.index("=") + 1:]
    mpstatOutput = subprocess.check_output(['mpstat']) # cpu usage

    mpstatLines = mpstatOutput.splitlines()
    cpuUsers = mpstatLines[2].split()
    cpuUsers = [x.decode() for x in cpuUsers]
    cpuUsage = mpstatLines[3].split()
    cpuUsage = [x.decode() for x in cpuUsage]

    # usageObject = {}
    # usageObject["idle"] = cpuUsage[cpuUsers.index("%idle")]

    # usageObjectJson = json.dumps(usageObject)

    #create json object
    # outputObject = {
    #     "t": str(cpu.temperature),
    #     "c": str(clockOutput),
    #     "v": str(voltsOutput),
    #     "cpu": str(usageObjectJson),
    # }

    print(cpu.temperature, end=",")

    clock = round(int(clockOutput) / 1000000000.0, 2)
    print(clock, end=",")

    print(str(voltsOutput)[:-1], end=",")

    usage = round(100 - float(cpuUsage[cpuUsers.index("%idle")]), 2)
    print(usage)

    # output json object
    # outputJSON = json.dumps(outputObject)
    # print(outputJSON)


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

# 3. MPU6050 - print accel, gyro, temp
def mpu6050():
    i2c = board.I2C()  # defaults 0x68
    mpu = adafruit_mpu6050.MPU6050(i2c)

    temp_offset = -8

    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
    print("Temperature (MPU): %.2f C" % (mpu.temperature + temp_offset))


get_cpu_temp()
camera()
mpu6050()