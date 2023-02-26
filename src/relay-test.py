import time
import gpio as GPIO

# set to relay IN GPIO # (not the pin number)
pin = 23
GPIO.setup(pin, GPIO.OUT)

while True:
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1.0)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1.0)