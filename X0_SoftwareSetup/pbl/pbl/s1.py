# `pbl.s1`: Code that's specific to PBL's sensor 1 (S1) lab.

import pbl.common

import os
import subprocess
import unittest

# tests that check that the Pi has been setup correctly for S1
class Tests(unittest.TestCase):

    def test_raspberry_pi_camera_interface_is_enabled(self):
        assert subprocess.run(["raspi-config", "nonint", f"get_camera"], check=True, capture_output=True, text=True).stdout.strip() == "0"

    def test_can_import_matplotlib(self):
        assert pbl.common.can_import("matplotlib")

    def test_can_import_guizero(self):
        assert pbl.common.can_import("guizero")

    def test_can_import_picamera(self):
        assert pbl.common.can_import("picamera")

    def test_coral_example_dir_is_installed(self):
        assert os.path.exists("/opt/coral_example")
        assert os.path.isdir("/opt/coral_example")

    def test_coral_example_has_expected_format(self):
        # these files are used when the students try out a test image classification on
        # a picture of a macaw
        assert os.path.isfile("/opt/coral_example/classify_image.py")
        assert os.path.isfile("/opt/coral_example/mobilenet_v2_1.0_224_inat_bird_quant.tflite")
        assert os.path.isfile("/opt/coral_example/inat_bird_labels.txt")
        assert os.path.isfile("/opt/coral_example/parrot.jpg")

        # same as above, but using the edgetpu model
        assert os.path.isfile("/opt/coral_example/classify_image.py")
        assert os.path.isfile("/opt/coral_example/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite")
        assert os.path.isfile("/opt/coral_example/inat_bird_labels.txt")
        assert os.path.isfile("/opt/coral_example/parrot.jpg")

    def test_posenet_code_dir_is_installed(self):
        assert os.path.exists("/opt/project-posenet")
        assert os.path.isdir("/opt/project-posenet")

    def test_posenet_has_expected_format(self):
        assert os.path.isfile("/opt/project-posenet/pose_camera.py")

class HardwareTests(unittest.TestCase):

    def test_can_show_webcam_footage(self):
        # copy+paste of what the students do while setting up for s1
        subprocess.run(["python3", "-m", "pbl.s1_test_webcam"], check=True)

    def test_can_infer_macaw_using_tflite_software_backend(self):
        # copy+paste of what the students do to check if tensorflow works without the coral thing
        subprocess.run(["python3", "classify_image.py", "--model", "mobilenet_v2_1.0_224_inat_bird_quant.tflite", "--labels", "inat_bird_labels.txt", "--input", "parrot.jpg"], cwd="/opt/coral_example", check=True)

    def test_can_infer_macaw_using_tflite_coral_backend(self):
        # copy+paste of what the students do to check if tensorflow works with coral dongle
        subprocess.run(["python3", "classify_image.py", "--model", "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite", "--labels", "inat_bird_labels.txt", "--input", "parrot.jpg"], cwd="/opt/coral_example", check=True)
