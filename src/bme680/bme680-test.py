import adafruit_bme680
import time
import board

# on 0x77

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()   # defaults 0x77
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
# bme680.sea_level_pressure = 1013.25

temperature = bme680.temperature
gas = bme680.gas
relative_humidity = bme680.relative_humidity
pressure = bme680.pressure
altitude = bme680.altitude

temp_offset = -7.0

while True:
    print("Temperature:", bme680.temperature + temp_offset, " \0C")
    print("Gas:", bme680.gas, "ohm")
    print("Relative Humidity:", bme680.relative_humidity)
    print("Pressure:", bme680.pressure, "hPa")
    print("Altitude:", bme680.altitude, "m")

    time.sleep(2)
