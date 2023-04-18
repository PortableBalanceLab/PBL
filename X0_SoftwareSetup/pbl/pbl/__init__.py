#!/usr/bin/env python3

# submodules of the course
import l2
import l3
import s1
import s2
import s3
import s4

# general libs
import sys
import subprocess

required_pi_interfaces = {
    "vnc",          # (how students typically access the Pi)
}

required_apt_packages = {
    "git",          # for clone-ing examples etc.
    "python3-pip",  # for installing python packages
    "mu-editor",    # recommended to students for editing code
    "thonny",       # recommended to students for editing code (alternative)
}

required_pip_packages = {
    "matplotlib",   # almost all lectures/practicals may use this, so always install it
    "numpy",        # TAs etc. may suggest it as a useful tool during lab sessions
}

# all modules that should be configured+installed by this top-level package
_all_modules = {sys.modules[__name__], l2, l3, s1, s2, s3, s4}

def _printing_subprocess_run(args, *other_args, **kwargs):
    print(f"running: {' '.join(args)}")
    return subprocess.run(args, *other_args, **kwargs)

# returns the set called `set_identifier` from `module`, or an empty set if not found
def _try_get_module_string_set(module, set_identifier):
    if hasattr(module, set_identifier):
        return getattr(module, set_identifier)
    else:
        return set()  # if it isn't defined, treat it as an empty set, rather than being missing

# returns the union of all sets called `set_identifier` from a sequence of `modules`
def _get_union_of_module_string_sets(modules, set_identifier):
    rv = set()
    for module in modules:
        rv = rv.union(_try_get_module_string_set(module, set_identifier))
    return rv

# returns the state (boolean) of one particular hardware interface on the Pi
def _get_pi_interface_state(interface_name):
    value = _printing_subprocess_run(["raspi-config", "nonint", f"get_{interface_name}"], check=True, capture_output=True, text=True).stdout.strip()
    return value == "0"  # 0 means "on" in Pi-land

# sets the state (boolean) of one particular hardware interface on the Pi
def _set_pi_interface_state(interface_name, desired_state):
    state_str = "0" if desired_state else "1"  # 0 means "on" in Pi-land
    _printing_subprocess_run(["dir", "raspi-config", f"set_{interface_name}", state_str])

# enables one particular hardware interface on the Pi
def _enable_pi_interface(interface_name):
    print(f"enabling {interface_name}")
    was_enabled = _get_pi_interface_state(interface_name)
    _set_pi_interface_state(interface_name)
    is_enabled = _get_pi_interface_state(interface_name)
    print(f"enabled {interface_name}: was_enabled = {was_enabled}, is_enabled = {is_enabled}")

# configures the Pi's hardware interfaces ready for PBL
def configure_pi_interfaces():
    print("----- starting configuring pi interfaces -----")
    for interface_name in _get_union_of_module_string_sets(_all_modules, "required_pi_interfaces"):
        _enable_pi_interface(interface_name)
    print("----- finished configuring pi interfaces -----")

# installs all APT dependencies used in PBL
def install_apt_dependencies():
    print("----- starting install apt dependencies -----")
    deps = _get_union_of_module_string_sets(_all_modules, "required_apt_packages")
    _printing_subprocess_run(["apt-get", "install", *deps], check=True)
    print("----- finished install apt dependencies -----")

# installs all PIP dependencies used in PBL
def install_pip_dependencies():
    print("----- starting install pip dependencies -----")
    deps = _get_union_of_module_string_sets(_all_modules, "required_pip_packages")
    _printing_subprocess_run(["pip", "install", *deps])
    print("----- finished install pip dependencies -----")

# tries to run one `on_custom_install` step for one PBL module
def _try_run_custom_install_step(module):
    try:
        module.on_custom_install()
    except AttributeError:
        print(f"{module.__name__}: has no on_custom_install method: skipping")

# tries to run all `on_custom_install` steps for all PBL modules
def run_custom_install_steps():
    for module in _all_modules:
        _try_run_custom_install_step(module)

# installs all software used by PBL practicals
def install_required_software():
    print("----- starting installing required software")
    install_apt_dependencies()
    install_pip_dependencies()
    run_custom_install_steps()
    print("----- finished installing required software")

# configures + installs the Pi ready for PBL
def setup():
    print("----- starting setup of Pi for PBL -----")
    configure_pi_interfaces()
    install_required_software()
    print("----- finished setup of Pi for PBL: enjoy :> -----")

# command-line entrypoint
def main():
    setup()

if __name__ == '__main__':
    main()
