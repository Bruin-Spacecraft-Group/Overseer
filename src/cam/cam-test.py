from picamera import PiCamera

camera = PiCamera()

camera.start_preview()
camera.start_recording('video.h264')
camera.wait_recording(5)
camera.stop_recording()
camera.stop_preview()