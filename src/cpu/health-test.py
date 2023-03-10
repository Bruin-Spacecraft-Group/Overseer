from gpiozero import CPUTemperature

# get cpu temperature
cpu = CPUTemperature()
print("CPU Temperature: " + str(cpu.temperature))

import subprocess

clockOutput = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']) # clock
voltsOutput = subprocess.check_output(['vcgencmd', 'measure_volts', 'core']) # cpu voltage
mpstatOutput = subprocess.check_output(['mpstat']) # cpu usage

mpstatLines = mpstatOutput.splitlines()
print(mpstatLines[3])
cpuUsers = mpstatLines[2].split()
cpuUsage = mpstatLines[3].split()

usageObject = {}

for i in range(4, min(7, len(cpuUsers))):
    usageObject[cpuUsers[i][1:]] = cpuUsage[i]

usageObjectJson = json.dumps(usageObject)

print(usageObjectJson)

print(cpuUsers)
print(cpuUsage)


import json

#create json object
outputObject = {
    "temp": str(cpu.temperature),
    "c": str(clockOutput),
    "v": str(voltsOutput),
    "top": str(usageObjectJson),
}

# output json object
outputJSON = json.dumps(outputObject)
print(outputJSON)