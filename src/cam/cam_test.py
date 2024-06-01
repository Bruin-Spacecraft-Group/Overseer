from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from datetime import datetime
import time

class MyCamera:
    def __init__(self):
        self.camera = Picamera2()
        self.camera.configure(self.camera.create_still_configuration(main={"size": (1920, 1080)}))
        self.cam_data = {}

    #TODO: for future years would recommend making separate take picture and record video functions
    def record_video(self, vid_fname, pic_fname, should_record):
        # Take a picture
        self.camera.start()
        self.camera.capture_file(pic_fname)
        self.camera.stop()

        # set return dictionary
        self.cam_data['pic_fname'] = pic_fname

        # Only records if main method specifies we should
        self.cam_data['vid_fname'] = 'n'
        if should_record:
            # Record and save video
            self.camera.configure(self.camera.create_video_configuration(main={"size": (1920, 1080)}))
            self.camera.start()
            encoder = H264Encoder(bitrate=10000000)
            self.camera.start_recording(encoder, vid_fname)
            time.sleep(10)
            self.camera.stop_recording()
            self.camera.stop()

            #add video file to return dict if created
            self.cam_data['vid_fname'] = vid_fname

        return self.cam_data

    def __del__(self):
        self.camera.close()

def main():
    # Initialize MyCamera instance
    camera = MyCamera()
    
    # Set the filenames for the video and picture
    vid_fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".h264"
    pic_fname = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".jpg"
    
    # Record video and take a picture
    reached_threshold = camera.record_video(vid_fname, pic_fname, True)
    
    # Print the result
    if reached_threshold:
        print(f"Video has been recorded and saved as {vid_fname}")
    else:
        print(f"Video was not recorded because the altitude threshold was not met.")

if __name__ == "__main__":
    main()
