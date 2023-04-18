required_apt_packages = {
    "git",              # for `clone`ing `hx711-multi`
    "automake",         # for `autoconf`
    "build-essential",  # ensures there's a C/C++ toolchain available
    "python3-tk",       # used by `guizero` (L3 and S1) for rendering the GUI
}

HX711_REPO="https://github.com/PortableBalanceLab/hx711-multi"

# installs hx711-multi library into the python environment
#
# it's used for reading data from the ADC
def _install_hx711multi():
    pass