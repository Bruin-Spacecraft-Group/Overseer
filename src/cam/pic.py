# take a pic using the camera and save it to the current folder

from datetime import datetime
from picamera import PiCamera

# def take_pic():
#     with PiCamera() as camera:
#         camera.resolution = (1024, 768)
#         camera.start_preview()
#         time.sleep(2)
#         name
#         camera.capture('image.jpg')


# if __name__ == '__main__':
#     take_pic()


camera = PiCamera()
# take a picture
fname = datetime.now().strftime("%H-%M-%S") + ".jpg"
camera.start_preview()
camera.capture(fname)
camera.stop_preview()
