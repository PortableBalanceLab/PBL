# content here is specific to S3

import pbl.common
from pbl.common import run_in_terminal, print_dir_contents

import os
import shutil
import tempfile
import unittest


required_apt_packages = {
    "git",              # for `clone`ing `hx711-multi`
    "automake",         # for `autoconf`
    "build-essential",  # ensures there's a C/C++ toolchain available
    "python3-tk",       # used by `guizero` (L3 and S1) for rendering the GUI
}

HX711_REPO="https://github.com/PortableBalanceLab/hx711-multi"

def on_custom_install():
    _install_hx711multi()

# installs hx711-multi library into the python environment
#
# it's used for reading data from the ADC
def _install_hx711multi():
    print("starting installing hx711multi")
    with tempfile.TemporaryDirectory() as temp_dir:

        # clone hx711multi source code
        run_in_terminal(f"git clone '{HX711_REPO}' hx711-multi/", cwd=temp_dir)

        # copy the source code to `/opt/hx711multi`, because S3 asks students to run the
        # `calibrate.py` script in it (/opt/hx711multi/tests/calibrate.py)
        if os.path.exists("/opt/hx711-multi"):
            shutil.rmtree("/opt/hx711-multi")  # remove existing install

        # install newer code
        shutil.copytree(os.path.join(temp_dir, "hx711-multi"), "/opt/hx711-multi")

        # also, install it system-wide as a `pip` package, so that students can
        # write `import hx711_multi.hx711` in their code, regardless of where they
        # saved their code
        run_in_terminal("pip3 install /opt/hx711-multi")

    print_dir_contents("/opt/hx711-multi")
    print("finished installing hx711multi")

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
