# content here is common to all parts of the PBL course

import importlib.util
import shutil
import subprocess
import unittest

required_pi_interfaces = {
    "vnc",          # (how students typically access the Pi)
}

required_apt_packages = {
    "git",                 # for clone-ing examples etc.
    "python3-pip",         # for installing python packages
    "mu-editor",           # recommended to students for editing code
    "thonny",              # recommended to students for editing code (alternative)
    "realvnc-vnc-server",  # so the Pi can host a VNC interface (#43 #44)
}

required_pip_packages = {
    "matplotlib",   # suggested in L2 and used by many lectures/practicals
    "numpy",        # suggested in L2 and may be recommended by TAs etc.
}

# run `cmd` as as-if running it in a terminal
def run_in_terminal(cmd, cwd=None):
    print(f"running: {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=True, cwd=cwd)

# prints the contents of the given directory path for inspection
def print_dir_contents(path):
    print(f"printing {path} contents")
    run_in_terminal(f"ls -la {path}")

def can_import(module_name_str):
    return importlib.util.find_spec(module_name_str) is not None

def module_has_attr(module_name_str, attr_name):
    spec = importlib.util.find_spec(module_name_str)
    if spec:
        module = spec.loader.load_module()
        return hasattr(module, attr_name)
    else:
        return False

# tests that check that the Pi has been setup correctly for L2
class Tests(unittest.TestCase):

    def test_vnc_is_enabled(self):
        assert subprocess.run(["raspi-config", "nonint", f"get_vnc"], check=True, capture_output=True, text=True).stdout.strip() == "0"

    def test_can_import_matplotlib(self):
        assert can_import("matplotlib")

    def test_can_import_numpy(self):
        assert can_import("numpy")

    def test_pip_available_on_command_line(self):
        assert shutil.which("pip") is not None

    def test_mu_available_on_command_line(self):
        assert shutil.which("mu-editor") is not None

    def test_thonny_available_on_command_line(self):
        assert shutil.which("thonny") is not None
