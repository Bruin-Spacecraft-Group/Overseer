# automatic

import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)


while True:
	# Cuts down the balloon if the incoming message if conditions are met
	if(altitude>80000 && x_pos && y_pos):
		print('Cutting Down The Balloon')

		# Cut down the balloon
		GPIO.output(23, GPIO.HIGH)
		time.sleep(120)
		GPIO.output(23, GPIO.LOW)
		time.sleep(120)
