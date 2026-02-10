# `pbl.l3`: Code that's specific to PBL's lecture 3 (L3).

import pbl.common

import unittest

# tests that check that the Pi has been set up correctly for L3
class Tests(unittest.TestCase):

    def test_can_import_guizero(self):
        assert pbl.common.can_import("guizero")

    def test_can_import_IPython_display(self):
        assert pbl.common.can_import("IPython.display")

    def test_can_import_gpiozero(self):
        assert pbl.common.can_import("gpiozero")
