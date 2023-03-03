# main


# 1. CPU Health
from datetime import datetime
from picamera import PiCamera
from gpiozero import CPUTemperature
import json
import subprocess

# 1. CPU Health
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


# 2. Camera
def camera():
    camera = PiCamera()

    # record 5 seconds
    # camera.start_preview()
    # camera.start_recording('video.h264')
    # camera.wait_recording(5)
    # camera.stop_recording()
    # camera.stop_preview()

    # take a picture
    fname = datetime.now().strftime("%H%M%S") + ".jpg"
    camera.start_preview()
    camera.capture(fname)
    camera.stop_preview()
