# content here is specific to L3

import pbl.common

import unittest

required_apt_packages = {
    "python3-tk",  # used by `guizero` for rendering the GUI
}

required_pip_packages = {
    "guizero",     # used to build GUIs in the lecture
    "gpiozero",    # used to blink and LED in the lecture
}

# tests that check that the Pi has been setup correctly for L3
class Tests(unittest.TestCase):

    def test_can_import_guizero(self):
        assert pbl.common.can_import("guizero")

    def test_can_import_IPython_display(self):
        assert pbl.common.can_import("IPython.display")

    def test_can_import_gpiozero(self):
        assert pbl.common.can_import("gpiozero")
