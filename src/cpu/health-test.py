from gpiozero import CPUTemperature

# get cpu temperature
cpu = CPUTemperature()

import subprocess
import json

clockOutput = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode()[:-1] # clock
voltsOutput = subprocess.check_output(['vcgencmd', 'measure_volts', 'core']).decode()[:-1] # cpu voltage
mpstatOutput = subprocess.check_output(['mpstat']) # cpu usage

mpstatLines = mpstatOutput.splitlines()
cpuUsers = mpstatLines[2].split()
cpuUsers = [x.decode() for x in cpuUsers]
cpuUsage = mpstatLines[3].split()
cpuUsage = [x.decode() for x in cpuUsage]

usageObject = {}

usageObject["usr"] = cpuUsage[cpuUsers.index("%nice")]
usageObject["sys"] = cpuUsage[cpuUsers.index("%sys")]
usageObject["idle"] = cpuUsage[cpuUsers.index("%idle")]

usageObjectJson = json.dumps(usageObject)

#create json object
outputObject = {
    "temp": str(cpu.temperature),
    "c": str(clockOutput),
    "v": str(voltsOutput),
    "cpu": str(usageObjectJson),
}

# output json object
outputJSON = json.dumps(outputObject)
print(outputJSON)