required_pi_interfaces = {
    "camera",      # for capturing images via the hardware ribbon interface
}

required_apt_packages = {
    "curl",        # for fetching GPG keys
    "wget",        # for downloading example model/script assets
    "git",         # for `clone`ing coral example models etc.
    "python3-tk",  # used by `guizero` for rendering the GUI
}

required_pip_packages = {
    "guizero",     # used to build camera booth GUI
    "pillow",      # used for processing images (previously: called `python-imaging` in apt)
}

PROJECT_POSENET_REPO="https://github.com/PortableBalanceLab/project-posenet"

# performs custom install steps (i.e. steps that aren't just pi interfaces, or
# installing off-the-shelf packages)
def on_custom_install():
    _install_coral()
    _install_coral_example()

# downloads+installs all TPU runtime coral.ai libraries
# needed to make the neural network camera work (for S1)
#
# pulled from: https://coral.ai/docs/accelerator/get-started
def _install_coral():
    pass

# installs extra coral test model data + script that shows
# the students a basic classification example in S1
#
# examples used in S1 are from: https://github.com/google-coral/tflite/tree/master/python/examples/classification
def _install_coral_example():
    # this code is based on https://github.com/google-coral/tflite
    #
    # see dir: `python/examples/classification`, which contains: `install_requirements.sh`

    pass

# installs posenet source code that the students
# modify in S1 to create their camera booth
def _install_posenet_code():
    pass
