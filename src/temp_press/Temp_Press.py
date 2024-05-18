# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import adafruit_bme680

# Create sensor object, communicating over the board's default I2C bus


class TempPress:
    def __init__(self):
        i2c = board.I2C()  # uses board.SCL and board.SDA
        # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
        self.bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

        # change this to match the location's pressure (hPa) at sea level
        self.bme680.sea_level_pressure = 1013.25

        # You will usually have to add an offset to account for the temperature of
        # the sensor. This is usually around 5 degrees but varies by use. Use a
        # separate temperature sensor to calibrate this one.
        self.temperature_offset = -5

    def record_tp(self):
        print("\nTemperature: %0.1f C" % (self.bme680.temperature + self.temperature_offset))
        print("Gas: %d ohm" % self.bme680.gas)
        print("Humidity: %0.1f %%" % self.bme680.relative_humidity)
        print("Pressure: %0.3f hPa" % self.bme680.pressure)
        print("Altitude = %0.2f meters" % self.bme680.altitude)

    
    time.sleep(1)
