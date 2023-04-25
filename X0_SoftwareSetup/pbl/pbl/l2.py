# content here is specific to L1

import pbl.common

import unittest

required_pip_packages = {
    "numpy",  # recommended to students in the lecture notes
}

# tests that check that the Pi has been setup correctly for L2
class Tests(unittest.TestCase):

    def test_can_import_matplotlib(self):
        assert pbl.common.can_import("matplotlib")
        assert pbl.common.can_import("matplotlib.pyplot")

    def test_can_import_numpy(self):
        assert pbl.common.can_import("numpy")

    def test_can_import_pickle(self):
        assert pbl.common.can_import("pickle")

    def test_can_import_json(self):
        assert pbl.common.can_import("json")
