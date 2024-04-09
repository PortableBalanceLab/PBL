# content here is specific to S1

import pbl.common
from pbl.common import run_in_terminal, print_dir_contents

import os
import shutil
import subprocess
import tempfile
import unittest
import urllib.request


required_pi_interfaces = {
    "camera",      # for capturing images via the hardware ribbon interface
}

required_apt_packages = {
    "curl",        # for fetching GPG keys
    "wget",        # for downloading example model/script assets
    "git",         # for `clone`ing coral example models etc.
    "python3-tk",  # used by `guizero` for rendering the GUI

    # these apt dependencies are from coral-edgetpu apt source
    "python3-tflite-runtime",
    "libedgetpu1-std",
    "python3-pycoral",
}

required_pip_packages = {
    "guizero",         # used to build camera booth GUI
    "pillow",          # used for processing images (previously: called `python-imaging` in apt)
}

PROJECT_POSENET_REPO="https://github.com/PortableBalanceLab/project-posenet"

# ensures coral-edgetpu-stable apt source is setup
def on_before_apt():
    # ensure coral-edgetpu-stable apt source is installed before
    # apt-installing the necessary dependencies
    #
    # pulled from: https://coral.ai/docs/accelerator/get-started

    run_in_terminal('echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list')
    run_in_terminal('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')
    run_in_terminal('sudo apt update')

# performs custom install steps (i.e. steps that aren't just pi interfaces, or
# installing off-the-shelf packages)
def on_custom_install():
    _install_coral_example()
    _install_posenet_code()

# installs extra coral test model data + script that shows
# the students a basic classification example in S1
#
# examples used in S1 are from: https://github.com/google-coral/tflite/tree/master/python/examples/classification
def _install_coral_example():
    # this code is based on https://github.com/google-coral/tflite
    #
    # see dir: `python/examples/classification`, which contains: `install_requirements.sh`

    print("starting installing coral test model data + scripts")

    # define which model/data assets are being downloaded (and from where)
    base_url = "https://github.com/google-coral/edgetpu/raw/master/test_data"
    assets = [
        "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite",  # hardware tensorflow-lite model
        "mobilenet_v2_1.0_224_inat_bird_quant.tflite",          # software tensorflow-lite model
        "inat_bird_labels.txt",                                 # labels
        "parrot.jpg",                                           # input image
    ]

    # write example assets to a local temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print("downloading model/data assets")
        for asset in assets:
            url = f"{base_url}/{asset}"
            asset_local_filepath = os.path.join(temp_dir, asset)
            urllib.request.urlretrieve(url, asset_local_filepath)

        # also, download `classify.py` and `classify_image.py` (these are what the students run)
        print("downloading classify.py and classify_image.py")
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify.py", os.path.join(temp_dir, "classify.py"))
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify_image.py", os.path.join(temp_dir, "classify_image.py"))

        # set correct permissions for dir + data (must be student-accessible from /opt/ without sudo etc.)
        os.chmod(temp_dir, 0o755)
        for asset_file in os.listdir(temp_dir):
            os.chmod(os.path.join(temp_dir, asset_file), 0o644)

        print("printing temporary directory contents")
        run_in_terminal(f"ls -la {temp_dir}")

        if os.path.exists("/opt/coral_example"):
            shutil.rmtree("/opt/coral_example")  # remove existing install
        # install new example code
        shutil.copytree(temp_dir, "/opt/coral_example")

    print_dir_contents("/opt/coral_example")
    print("finished installing coral test model data + scripts")

# installs posenet source code that the students
# modify in S1 to create their camera booth
def _install_posenet_code():
    print("starting install_posenet_code")

    with tempfile.TemporaryDirectory() as temp_dir:
        run_in_terminal(f"git clone --depth=1 '{PROJECT_POSENET_REPO}' project-posenet/", cwd=temp_dir)

        # install requirements (required to actually run it)
        run_in_terminal("./project-posenet/install_requirements.sh", cwd=temp_dir)

        # install into /opt/project-posenet, which is where students are told to find it
        run_in_terminal("sudo rm -rf /opt/project-posenet", cwd=temp_dir)
        run_in_terminal("sudo cp -ra project-posenet /opt/project-posenet", cwd=temp_dir)

    print_dir_contents("/opt/project-posenet")
    print("finished install_posenet_code")

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

    # TODO: test posenet pose_camera.py can be ran etc. - it's a hardware test, though
