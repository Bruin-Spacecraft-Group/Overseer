from picamera2 import Picamera2 as PiCamera
from datetime import datetime

class MyCamera:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (1920, 1080)

    def record_video(self, vid_fname, pic_fname, altitude, reached_threshold):
        #takes image
        self.camera.start_preview()
        self.camera.capture(pic_fname)
        self.camera.stop_preview()

        #checks if we reached 100 feet and if video not already taken
        if altitude >= 100 and not reached_threshold:
            #records and saves video
            self.camera.start_preview()
            self.camera.start_recording(vid_fname)
            self.camera.wait_recording(10)
            self.camera.stop_recording()
            self.camera.stop_preview()

            #so we don't try recording again
            reached_threshold = True

        return reached_threshold
    
    def __del__(self):
        self.camera.close()

def main():
    # Initialize MyCamera instance
    camera = MyCamera()
    
    # Set the filenames for the video and picture
    vid_fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h264"
    pic_fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
    # Set the altitude and initial reached_threshold state
    altitude = 150  # Example altitude in feet
    reached_threshold = False
    
    # Record video and take a picture
    reached_threshold = camera.record_video(vid_fname, pic_fname, altitude, reached_threshold)
    
    # Print the result
    if reached_threshold:
        print(f"Video has been recorded and saved as {vid_fname}")
    else:
        print(f"Video was not recorded because the altitude threshold was not met.")

if __name__ == "__main__":
    main()
