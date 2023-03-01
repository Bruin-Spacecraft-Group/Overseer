import adafruit_bme680
import time
import board

# on 0x77

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C() # defualts 0x77
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1014.22

temperature = bme680.temperature
gas = bme680.gas
relative_humidity = bme680.relative_humidity
pressure = bme680.pressure
altitude = bme680.altitude

temp_offset = 0

print("Temperature: %0.1f C" % (bme680.temperature + temp_offset))
print("Gas Resistance: %d ohm" % bme680.gas)
print("Relative Humidity: %0.1f %%" % bme680.relative_humidity)
print("Pressure: %0.3f hPa" % bme680.pressure)
print("Altitude = %0.2f meters" % bme680.altitude)

time.sleep(2)
