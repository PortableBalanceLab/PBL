# content here is common to all parts of the PBL course

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

# run `cmd` as as-if running it in a terminal
def run_in_terminal(cmd, cwd=None):
    print(f"running: {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=True, cwd=cwd)

# prints the contents of the given directory path for inspection
def print_dir_contents(path):
    print(f"printing {path} contents")
    run_in_terminal(f"ls -la {path}")
