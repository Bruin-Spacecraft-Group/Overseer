import time
import board
import adafruit_mpu6050

i2c = board.I2C(0x68)  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (mpu.gyro))
print("Temperature: %.2f C" % mpu.temperature)
print("")
time.sleep(1)
