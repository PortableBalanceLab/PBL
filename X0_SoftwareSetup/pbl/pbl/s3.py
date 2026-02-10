# `pbl.s3`: Code that's specific to PBL's sensor 3 (S3) lab.

import pbl.common

import os
import unittest

# tests that check that the Pi has been setup correctly for S2
class Tests(unittest.TestCase):

    def test_can_import_hx711_multi(self):
        assert pbl.common.can_import("hx711_multi")
    
    def test_can_import_hx711_multi_hx711_module(self):
        assert pbl.common.can_import("hx711_multi.hx711")
    
    def test_can_import_HX711_class(self):
        assert pbl.common.module_has_attr("hx711_multi", "HX711")
        assert pbl.common.module_has_attr("hx711_multi.hx711", "HX711")

    def test_hx711_multi_is_available_in_opt(self):
        assert os.path.exists("/opt/hx711-multi")
        assert os.path.isdir("/opt/hx711-multi")

    def test_hx711_multi_contains_an_identify_script(self):
        assert os.path.isfile("/opt/hx711-multi/tests/identify.py")

    def test_hx711_multi_contains_a_calibrate_script(self):
        assert os.path.isfile("/opt/hx711-multi/tests/calibrate.py")

    def test_can_import_RPi_GPIO_module(self):
        assert pbl.common.can_import("RPi.GPIO")

    def test_can_import_matplotlib(self):
        assert pbl.common.can_import("matplotlib")

    def test_can_import_matplotlib_animation_module(self):
        # because the lab requires students to create an animated plot
        assert pbl.common.can_import("matplotlib.animation")
