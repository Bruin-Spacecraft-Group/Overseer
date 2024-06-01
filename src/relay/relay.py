from time import sleep
from gpiozero import LED



class Relay:
    def __init__(self):
        # set to relay IN GPIO # (not the pin number)
        self.pin = LED(27)

    def cutdown(self, cut_threshold):
        msg = ""

        if cut_threshold:
            #TODO: see how long it takes for the nichrome wire to heat up enough - adjust for high altitude
            self.pin.on()
            sleep(5)
            self.pin.off()
            msg = "cutdown"

        return msg


def main():
    # Create an instance of the Relay class
    relay = Relay()

    # Execute the cutdown method
    cut_threshold = True
    result = relay.cutdown(cut_threshold)

    # Print the result
    print(result)

if __name__ == "__main__":
    main()
