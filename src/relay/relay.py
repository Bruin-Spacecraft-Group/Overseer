from time import sleep
from gpiozero import LED



class Relay:
    def __init__(self):
        # set to relay IN GPIO # (not the pin number)
        self.pin = LED(27)
        self.cutdown_data = {}

    def cutdown(self, cut_threshold):
        self.cutdown_data['msg'] = ""

        if cut_threshold:
            #TODO: see how long it takes for the nichrome wire to heat up enough - adjust for high altitude
            self.pin.on()
            sleep(20)
            self.pin.off()
            self.cutdown_data['msg'] = "cutdown"

        return self.cutdown_data


def main():
    # Create an instance of the Relay class
    relay = Relay()

    # Execute the cutdown method
    sleep(5)
    cut_threshold = True
    result = relay.cutdown(cut_threshold)

    # Print the result
    print(result)

if __name__ == "__main__":
    main()
