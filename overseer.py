import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = .5)

while True:
	ser.write(str.encode('Hello User'))
	incoming = ser.readline().strip()
	if(incoming == 'cutdown'):
		print('Cutting Down The Balloon')
	print ('Received: ' + incoming)
