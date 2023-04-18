# content here is specific to S2

import pbl.common
from pbl.common import run_in_terminal, print_dir_contents

import os
import shutil
import tempfile
import unittest


required_pi_interfaces = {
    "i2c",              # hardware interface used by the IMU? (legacy?)
}

required_apt_packages = {
    "git",              # for `clone`ing bcm2835 and icm20948
    "automake",         # for `autoconf`
    "build-essential",  # ensures there's a C/C++ toolchain available
}

required_pip_packages = {
    "RPi.GPIO",         # dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "spidev",           # dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "smbus",            # dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B)) (previously: called `python-smbus` in apt)
}

BCM2835_REPO = "https://github.com/PortableBalanceLab/bcm2835"
ICM20948_REPO="https://github.com/PortableBalanceLab/ICM20948"

def on_custom_install():
    _install_bcm2835()
    _install_icm20948()

# downloads+installs bcm2835 on the pi
#
# bcm2835 is used in S2 (IMU). The waveshare guide for SenseHAT
# mentions that it must be installed:
#     - https://www.waveshare.com/wiki/Sense_HAT_(B)
def _install_bcm2835():
    print("starting installing bcm2835")
    with tempfile.TemporaryDirectory() as temp_dir:
        # clone BCM2835 source code
        run_in_terminal(f"git clone '{BCM2835_REPO}' bcm2835/", cwd=temp_dir)

        # reconfigure: this is necessary, because `git` doesn't track timestamps from the original archive
        run_in_terminal("autoreconf -f -i", cwd=os.path.join(temp_dir, "bcm2835"))

        # configure, build, check, and install the library system-wide
        run_in_terminal("./configure && make && make check && make install", cwd=os.path.join(temp_dir, "bcm2835"))

    print("finished installing bcm2835")

# installs ICM20948.py, which is used in S2
def _install_icm20948():
    print("starting installing icm20948")
    with tempfile.TemporaryDirectory() as temp_dir:
        # clone ICM20948 source code
        run_in_terminal(f"git clone '{ICM20948_REPO}' ICM20948/", cwd=temp_dir)

        icm20948_script_path = os.path.join(temp_dir, "ICM20948", "ICM20948.py")

        # set permissions of the script accordingly
        os.chmod(icm20948_script_path, 0o644)

        # copy it into `/opt`, which is where S2 says students can find it
        shutil.copy(icm20948_script_path, "/opt/ICM20948.py")

    print_dir_contents("/opt")
    print("finished installing icm20948")

# tests that check that the Pi has been setup correctly for S2
class Tests(unittest.TestCase):

    def test_can_import_smbus(self):
        # used internally by ICM20948
        assert pbl.common.can_import("smbus")

    def test_ICM20948_is_in_opt(self):
        assert os.path.exists("/opt/ICM20948.py")
        assert os.path.isfile("/opt/ICM20948.py")

    def test_can_import_matplotlib(self):
        assert pbl.common.can_import("matplotlib")

    def test_can_import_matplotlib_animation_module(self):
        assert pbl.common.can_import("matplotlib.animation")