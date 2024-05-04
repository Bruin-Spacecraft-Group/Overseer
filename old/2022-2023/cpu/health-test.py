from gpiozero import CPUTemperature

# get cpu temperature
cpu = CPUTemperature()

import subprocess
import json
from decimal import Decimal


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

usageObject = {}

# usageObject["usr"] = cpuUsage[cpuUsers.index("%nice")]
# usageObject["sys"] = cpuUsage[cpuUsers.index("%sys")]
usageObject["idle"] = cpuUsage[cpuUsers.index("%idle")]

usageObjectJson = json.dumps(usageObject)

#create json object
outputObject = {
    "t": str(cpu.temperature),
    "c": str(clockOutput),
    "v": str(voltsOutput),
    "cpu": str(usageObjectJson),
}

# output json object
outputJSON = json.dumps(outputObject)
print(outputJSON)