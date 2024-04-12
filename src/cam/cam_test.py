from picamera import PiCamera
from datetime import datetime

class MyCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)

    def record_video(self, vid_fname, pic_fname, altitude, reached_threshold):
        #checks if we reached 100 feet and if video not already taken
        if altitude >= 100 and not reached_threshold:
            #records and saves video
            self.camera.start_preview()
            self.camera.start_recording(fname)
            self.camera.wait_recording(10)
            self.camera.stop_recording()
            self.camera.stop_preview()

            #so we don't try recording again
            reached_threshold = True

        return reached_threshold