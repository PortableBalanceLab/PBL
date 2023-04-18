import pbl.utils

import os
import shutil
import tempfile

required_pi_interfaces = {
    "i2c",              # hardware interface used by the IMU? (legacy?)
}

required_apt_packages = {
    "git",              # for `clone`ing bcm2835 and icm20948
    "automake",         # for `autoconf`
    "build-essential",  # ensures there's a C/C++ toolchain available
    "python3-tk",       # used by `guizero` (L3 and S1) for rendering the GUI
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
        pbl.utils.run_shell_command(f"git clone '{BCM2835_REPO}' bcm2835/", cwd=temp_dir)

        # reconfigure: this is necessary, because `git` doesn't track timestamps from the original archive
        pbl.utils.run_shell_command("autoreconf -f -i", cwd=os.path.join(temp_dir, "bcm2835"))

        # configure, build, check, and install the library system-wide
        pbl.utils.run_shell_command("./configure && make && make check && make install", cwd=os.path.join(temp_dir, "bcm2835"))

    print("finished installing bcm2835")

# installs ICM20948.py, which is used in S2
def _install_icm20948():
    print("starting installing icm20948")
    with tempfile.TemporaryDirectory() as temp_dir:
        # clone ICM20948 source code
        pbl.utils.run_shell_command(f"git clone '{ICM20948_REPO}' ICM20948/", cwd=temp_dir)

        icm20948_script_path = os.path.join(temp_dir, "ICM20948", "ICM20948.py")

        # set permissions of the script accordingly
        os.chmod(icm20948_script_path, 0o644)

        # copy it into `/opt`, which is where S2 says students can find it
        shutil.copy(icm20948_script_path, "/opt/ICM20948.py")

    print("finished installing icm20948")