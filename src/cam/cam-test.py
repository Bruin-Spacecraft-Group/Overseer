from picamera import PiCamera
from datetime import datetime

# sets up camera
camera = PiCamera()

#intializes (TODO altitude should be given)
alt = 0
reachedTreshold = False

#checks if we reached 200 feet, and if video not alr taken
if alt >= 200 and not reachedTreshold:
    #records and saves video
    fname = datetime.now().strftime("%H-%M-%S") + ".h264"
    camera.start_preview()
    camera.start_recording(fname)
    camera.wait_recording(25)
    camera.stop_recording()
    camera.stop_preview()

    #so we don't try recording again
    reachedTreshold = True


