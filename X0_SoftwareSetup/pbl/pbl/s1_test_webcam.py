# `pbl.s1_test_webcam`: one-off script that tests whether the PiCamera
# interface is actually working on the Raspberry Pi.

from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
sleep(5)
camera.stop_preview()

