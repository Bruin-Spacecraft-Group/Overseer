from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from datetime import datetime
import time

class MyCamera:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration(main={"size": (1920, 1080)}))

    #TODO: for future years would recommend making separate take picture and record video functions
    def record_video(self, vid_fname, pic_fname, altitude, reached_threshold):
        # Take a picture
        self.camera.start()
        self.camera.capture_file(pic_fname)
        self.camera.stop()

        # Check if we reached 100 feet and if video not already taken
        if altitude >= 100 and not reached_threshold:
            # Record and save video
            self.camera.configure(self.camera.create_video_configuration(main={"size": (1920, 1080)}))
            self.camera.start()
            encoder = H264Encoder(bitrate=10000000)
            self.camera.start_recording(encoder, vid_fname)
            time.sleep(10)
            self.camera.stop_recording()
            self.camera.stop()

            # So we don't try recording again
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
