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

# downloads+installs bcm2835 on the pi
#
# bcm2835 is used in S2 (IMU). The waveshare guide for SenseHAT
# mentions that it must be installed:
#     - https://www.waveshare.com/wiki/Sense_HAT_(B)
def _install_bcm2835():
    pass

# installs ICM20948.py, which is used in S2
def _install_icm20948():
    pass