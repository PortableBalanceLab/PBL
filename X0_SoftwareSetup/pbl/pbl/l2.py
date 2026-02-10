# `pbl.l2`: Code that's specific to PBL's lecture 2 (L2).

import pbl.common

import unittest

# tests that check that the Pi has been set up correctly for L2
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
