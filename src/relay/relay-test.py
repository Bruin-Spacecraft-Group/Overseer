from time import sleep
from gpiozero import LED

# set to relay IN GPIO # (not the pin number)
pin = LED(27)

while True:
    pin.on()
    sleep(2)
    pin.off()
    sleep(2)