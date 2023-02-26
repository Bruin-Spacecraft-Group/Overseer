import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = .5) 
	# Edit for USB port used

while True:
	# Debug
	ser.write(str.encode('Hello User'))

	# Receive incoming messages
	incoming = ser.readline().strip()
	print ('Received: ' + incoming)

	# Cuts down the balloon if the incoming message is the string 'cutdown'
	if(incoming == 'cutdown'):
		print('Cutting Down The Balloon')

		# Cut down the balloon
		GPIO.output(23, GPIO.HIGH)
		time.sleep(120)
		GPIO.output(23, GPIO.LOW)
		time.sleep(120)
