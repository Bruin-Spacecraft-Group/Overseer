from gpiozero import CPUTemperature

# get cpu temperature
cpu = CPUTemperature()
print("CPU Temperature: " + str(cpu.temperature))

import subprocess

clockOutput = subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']) # clock
voltsOutput = subprocess.check_output(['vcgencmd', 'measure_volts', 'core']) # cpu voltage
mpstatOutput = subprocess.check_output(['mpstat']) # cpu usage

mpstatLines = mpstatOutput.split("\n")
print(mpstatLines[3])
cpuUsers = mpstatLines[2].split()
cpuUsage = mpstatLines[3].split()

print(cpuUsers)
print(cpuUsage)


import json

#create json object
outputObject = {
    "temp": str(cpu.temperature),
    "c": str(clockOutput),
    "v": str(voltsOutput),
    "top": str(topOutput),
}

# output json object
outputJSON = json.dumps(outputObject)
print(outputJSON)