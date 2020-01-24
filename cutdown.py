#!/usr/bin/python
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# Pin number
relay_pin = 7

GPIO.setwarnings(False)

# Set the numbering mode
GPIO.setmode(GPIO.BOARD)

# Setup as output relay component
GPIO.setup(relay_pin, GPIO.OUT)
# Grab value from geofence.py and if it is true, then send a signal

def cut_down():
	GPIO.output(relay_pin, 0)
	time.sleep(.1)
	GPIO.output(relay_pin, 1)
	GPIO.cleanup()
