from picamera2 import Picamera2, Preview
from time import sleep
import libcamera

# create a camera
camera = Picamera2()

# configure it to show a preview
config = camera.create_preview_configuration()
config['transform'] = libcamera.Transform(vflip=True)
camera.configure(config)

# show the preview in a window (Qt)
camera.start_preview(Preview.QTGL)
camera.start()
sleep(5)  # sleep for 5 sec. to keep the window open
camera.stop_preview()
