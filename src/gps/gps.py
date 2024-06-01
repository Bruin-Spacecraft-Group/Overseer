#!/usr/bin/python3
import threading
import time
import io
import json
import fcntl
import smbus
try:
    import RPi.GPIO as GPIO
except:
    from mockgpio import MockGPIO as GPIO

# I2C Configuration
I2C_SLAVE = 0x0703
bus = 1
device = 0x42

# Navigation Command for Flight Mode
setNavCmnd = [0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x06,
              0x03, 0x00, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00,
              0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00, 0x64, 0x00, 0x2C,
              0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
              0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0xDC]

class CommunicationThread(threading.Thread):
    def __init__(self, onNMEA, onError):
        threading.Thread.__init__(self)
        self.onNMEA = onNMEA
        self.onError = onError
        self.isOk = False
        self.exitFlag = False

        # Setup I2C
        try:
            self.fr = io.open("/dev/i2c-" + str(bus), "r+b", buffering=0)
            self.fw = io.open("/dev/i2c-" + str(bus), "w+b", buffering=0)
            fcntl.ioctl(self.fr, I2C_SLAVE, device)
            fcntl.ioctl(self.fw, I2C_SLAVE, device)
            self.isOk = True
        except Exception as e:
            self.onError(f"GPS I2C error: {e}")

    def stop(self):
        self.exitFlag = True

    def send_bytes(self, buffer):
        data = bytearray(len(buffer))
        data[0:] = buffer[0:]
        try:
            self.fw.write(data)
        except Exception as e:
            self.onError(f"I2C write error: {e}")

    def read_byte(self):
        while not self.exitFlag:
            try:
                ch = self.fr.read(1)
                if ch:
                    return ch[0]
            except IOError:
                time.sleep(0.1)
        return 255

    def run(self):
        rxNMEA = False
        response = ""
        ch = ' '
        while not self.exitFlag:
            prev_ch = ch
            ch = self.read_byte()
            if rxNMEA:
                if ch in [10, 13]:
                    self.onNMEA(response)
                    response = ""
                    rxNMEA = False
                else:
                    response += chr(ch & 0x7f)
            elif ch == ord('$'):
                rxNMEA = True
                response = chr(ch)

class Ublox:
    def __init__(self):
        self.GPSDAT = {"status": "init", "lat": "0.00", "lon": "0.00", "alt": "0"}
        self.comm_thread = None
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def gps_reset(self):
        if self.comm_thread is not None:
            self.comm_thread.stop()
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, GPIO.LOW)
        time.sleep(1)
        GPIO.output(17, GPIO.HIGH)
        self.comm_thread = CommunicationThread(self.nmea_handler, self.error_handler)
        self.comm_thread.start()

    def start(self):
        self.gps_reset()

    def stop(self):
        self.comm_thread.stop()

    def get_data(self):
        return self.GPSDAT

    def nmea_handler(self, line):
        tokens = line.split(',')
        if tokens[0] == "$GNGGA":
            self.GPSDAT["lat"] = self.parse_lat_lon(tokens[2], tokens[3])
            self.GPSDAT["lon"] = self.parse_lat_lon(tokens[4], tokens[5])
            self.GPSDAT["alt"] = tokens[9]

    def parse_lat_lon(self, raw, direction):
        if raw == "":
            return 0.0
        degrees = int(raw[:2])
        minutes = float(raw[2:])
        decimal_degrees = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal_degrees = -decimal_degrees
        return decimal_degrees

    def error_handler(self, status):
        print(status)

if __name__ == "__main__":
    gps = Ublox()
    gps.start()
    try:
        while True:
            print(gps.get_data())
            time.sleep(5)
    except KeyboardInterrupt:
        gps.stop()
    print("Done.")
