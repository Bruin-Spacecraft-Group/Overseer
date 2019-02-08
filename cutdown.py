#!/usr/bin/python
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")


# pin number
relay_pin = 7

GPIO.setwarnings(False)

# different pin numbering depending on board
mode = GPIO.getmode()
# set the numbering mode
GPIO.setmode(mode)
# setup as output relay component
GPIO.setup(relay_pin, GPIO.OUT)
# grab value from geofence.py and if it is true send a signal
def cut_down():
		GPIO.output(relay_pin, 0)
		time.sleep(.1)
		GPIO.output(relay_pin, 1)
		GPIO.cleanup()
