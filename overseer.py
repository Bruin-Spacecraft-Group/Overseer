import serial
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = .5)

while True:
	ser.write(str.encode('Hello User'))
	incoming = ser.readline().strip()
	print ('Received: ' + incoming)

	if(incoming == 'cutdown'):
		print('Cutting Down The Balloon')
		GPIO.output(23, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(23, GPIO.LOW)
		time.sleep(3)
		
	
