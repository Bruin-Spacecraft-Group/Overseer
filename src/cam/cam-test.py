from picamera import PiCamera
from datetime import datetime

camera = PiCamera()

# record 5 seconds
# camera.start_preview()
# camera.start_recording('video.h264')
# camera.wait_recording(5)
# camera.stop_recording()
# camera.stop_preview()

# take a picture
fname = datetime.now().strftime("%H%M%S") + ".jpg"
camera.start_preview()
camera.capture(fname)
camera.stop_preview()
