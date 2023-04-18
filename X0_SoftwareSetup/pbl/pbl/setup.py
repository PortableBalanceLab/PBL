# content here relates to setting up a (potentially, fresh) Raspberry Pi ready for
# the PBL course

# components of the PBL course
import pbl.common
import pbl.l2
import pbl.l3
import pbl.s1
import pbl.s2
import pbl.s3
import pbl.s4

# general libs
import subprocess


# all modules that should be configured+installed by the setup process
_all_modules = {pbl.common, pbl.l2, pbl.l3, pbl.s1, pbl.s2, pbl.s3, pbl.s4}

def _printing_subprocess_run(args, *other_args, **kwargs):
    print(f"running: {' '.join(args)}", flush=True)
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
    _printing_subprocess_run(["raspi-config", "nonint", f"do_{interface_name}", state_str], check=True)

# enables one particular hardware interface on the Pi
def _enable_pi_interface(interface_name):
    print(f"enabling {interface_name}")
    was_enabled = _get_pi_interface_state(interface_name)
    _set_pi_interface_state(interface_name, True)
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

# tries to run one `on_custom_install` step for one PBL course component (e.g. s1)
def _try_run_custom_install_step(module):
    if hasattr(module, "on_custom_install"):
        print(f"--- starting {module.__name__}.on_custom_install() ---")
        getattr(module, "on_custom_install")()
        print(f"--- finished {module.__name__}.on_custom_install() ---")
    else:
        # print(f"{module.__name__}: has no on_custom_install method: skipping")
        pass

# tries to run all `on_custom_install` steps for all PBL course components
def run_custom_install_steps():
    for module in _all_modules:
        _try_run_custom_install_step(module)

# installs all software used by PBL course components
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
