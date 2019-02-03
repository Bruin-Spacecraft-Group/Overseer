#!/usr/bin/python
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

import geofence as gf

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
to_cut = gf.inorout(long, lat)
def cut_down(to_cut = false):
	if to_cut == True:
		GPIO.output(relay_pin, 0)
		time.sleep(.1)
		GPIO.output(relay_pin, 1)

if __name__ == '__main__':
	cut_down(to_cut)
	GPIO.cleanup()