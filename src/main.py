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

# 1. CPU Health - print temp, clock, volt, top


def get_cpu_temp():
    # get cpu temperature
    cpu = CPUTemperature()
    print("CPU Temperature: " + str(cpu.temperature))

    clockOutput = subprocess.check_output(
        ['vcgencmd', 'measure_clock', 'arm'])  # clock
    voltsOutput = subprocess.check_output(
        ['vcgencmd', 'measure_volts', 'core'])  # cpu voltage
    topOutput = subprocess.check_output(['mpstat'])  # cpu usage

    # create json object
    outputObject = {
        "temp": str(cpu.temperature),
        "c": str(clockOutput),
        "v": str(voltsOutput),
        "top": str(topOutput),
    }
    # output json object
    outputJSON = json.dumps(outputObject)
    print(outputJSON)


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
