import pbl.utils

import os
import shutil
import tempfile

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
        pbl.utils.run_shell_command(f"git clone '{HX711_REPO}' hx711-multi/", cwd=temp_dir)

        # copy the source code to `/opt/hx711multi`, because S3 asks students to run the
        # `calibrate.py` script in it (/opt/hx711multi/tests/calibrate.py)
        if os.path.exists("/opt/hx711-multi"):
            shutil.rmtree("/opt/hx711-multi")  # remove existing install

        # install newer code
        shutil.copytree(os.path.join(temp_dir, "hx711-multi"), "/opt/hx711-multi")

        # also, install it system-wide as a `pip` package, so that students can
        # write `import hx711_multi.hx711` in their code, regardless of where they
        # saved their code
        pbl.utils.run_shell_command("pip3 install /opt/hx711-multi")
    print("finished installing hx711multi")