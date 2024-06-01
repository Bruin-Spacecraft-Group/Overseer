import adafruit_mpu6050
import board
import time

class accelerometer:
    def __init__(self):
        self.i2c = board.I2C()
        self.mpu = adafruit_mpu6050.MPU6050(i2c);

    def mpu_data(self):
        dic = {'Acceleration': self.mpu.acceleration, 'Gyro': self.mpu.gyro, 'Temperature': self.mpu.temperature}
        return dic

def main():
    acc = accelerometer()
    
    try:
        while True:
            data = acc.mpu_data()
            print(f"Acceleration: {data['Acceleration']}")
            print(f"Gyro: {data['Gyro']}")
            print(f"Temperature: {data['Temperature']}")
            time.sleep(1)  # Delay for readability
    except KeyboardInterrupt:
        print("Program interrupted by the user.")
    finally:
        del acc

if __name__ == "__main__":
    main()
