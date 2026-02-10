# `pbl.s2`: Code that's specific to PBL's sensor 2 (S2) lab.

import pbl.common

import os
import unittest

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