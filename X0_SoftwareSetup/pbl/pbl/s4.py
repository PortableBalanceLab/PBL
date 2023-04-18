# content here is specific to S4

import pbl.common

import subprocess
import unittest

required_pi_interfaces = {
    "i2c",                             # hardware interface used by the lab
}

required_pip_packages = {
    "Adafruit-Blinka",                 # CircuitPython support
    "adafruit-circuitpython-ads1x15",  # library for the ADS1115 board
}

# tests that check that the Pi has been setup correctly for S2
class Tests(unittest.TestCase):

    def test_i2c_interface_is_enabled(self):
        assert subprocess.run(["raspi-config", "nonint", f"get_i2c"], check=True, capture_output=True, text=True).stdout.strip() == "0"

    def test_can_import_board(self):
        assert pbl.common.can_import("board")

    def test_can_import_busio(self):
        assert pbl.common.can_import("busio")

    def test_can_import_adafruit_ads1x15(self):
        assert pbl.common.can_import("adafruit_ads1x15")
