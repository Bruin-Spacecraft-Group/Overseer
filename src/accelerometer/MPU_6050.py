#import adafruit_mpu6050
import board
import adafruit_lsm303_accel
import time

class accelerometer:
    def __init__(self):
        self.i2c = board.I2C()
        self.mpu = adafruit_lsm303_accel.LSM303_Accel(self.i2c)

    def mpu_data(self):
        dic = {'Acceleration': self.mpu.acceleration, 'Gyro': self.mpu.gyro, 'Temperature': self.mpu.temperature}
        return dic