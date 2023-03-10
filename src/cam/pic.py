# take a pic using the camera and save it to the current folder

import picamera
import time


def take_pic():
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        time.sleep(2)
        camera.capture('image.jpg')


if __name__ == '__main__':
    take_pic()
