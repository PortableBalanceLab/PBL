import os
import shutil
import subprocess
import tempfile
import urllib.request

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
    "guizero",         # used to build camera booth GUI
    "pillow",          # used for processing images (previously: called `python-imaging` in apt)
    "tflite-runtime",  # used by the coral Edge TPU runtime (USB layer?)
}

PROJECT_POSENET_REPO="https://github.com/PortableBalanceLab/project-posenet"

# performs custom install steps (i.e. steps that aren't just pi interfaces, or
# installing off-the-shelf packages)
def on_custom_install():
    _install_coral_libraries()
    _install_coral_example()
    _install_posenet_code()

def _run_in_shell(cmd, cwd=None):
    print(f"running: {cmd}", flush=True)
    return subprocess.run(cmd, shell=True, check=True, cwd=cwd)

# downloads+installs all TPU runtime coral.ai libraries
# needed to make the neural network camera work (for S1)
#
# pulled from: https://coral.ai/docs/accelerator/get-started
def _install_coral_libraries():
    print("starting installing coral libraries")

    # install the Edge TPU runtime (USB layer)
    _run_in_shell('echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list')
    _run_in_shell('curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -')
    _run_in_shell('sudo apt update')
    _run_in_shell('sudo apt install -y libedgetpu1-std python3-pycoral')

    print("finished installing coral libraries")

# installs extra coral test model data + script that shows
# the students a basic classification example in S1
#
# examples used in S1 are from: https://github.com/google-coral/tflite/tree/master/python/examples/classification
def _install_coral_example():
    # this code is based on https://github.com/google-coral/tflite
    #
    # see dir: `python/examples/classification`, which contains: `install_requirements.sh`

    print("starting installing coral test model data + scripts")

    # define which model/data assets are being downloaded (and from where)
    base_url = "https://github.com/google-coral/edgetpu/raw/master/test_data"
    assets = [
        "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite",  # hardware tensorflow-lite model
        "mobilenet_v2_1.0_224_inat_bird_quant.tflite",          # software tensorflow-lite model
        "inat_bird_labels.txt",                                 # labels
        "parrot.jpg",                                           # input image
    ]

    # write example assets to a local temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print("downloading model/data assets")
        for asset in assets:
            url = f"{base_url}/{asset}"
            asset_local_filepath = os.path.join(temp_dir, asset)
            urllib.request.urlretrieve(url, asset_local_filepath)

        # also, download `classify.py` and `classify_image.py` (these are what the students run)
        print("downloading classify.py and classify_image.py")
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify.py", os.path.join(temp_dir, "classify.py"))
        urllib.request.urlretrieve("https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify_image.py", os.path.join(temp_dir, "classify_image.py"))

        # set correct permissions for dir + data (must be student-accessible from /opt/ without sudo etc.)
        os.chmod(temp_dir, 0o755)
        for asset_file in os.listdir(temp_dir):
            os.chmod(os.path.join(temp_dir, asset_file), 0o644)

        print("printing temporary directory contents")
        _run_in_shell(f"ls -la {temp_dir}")

        # remove any existing `coral_example` dir and copy this one over it
        shutil.rmtree("/opt/coral_example")
        shutil.copytree(temp_dir, "/opt/coral_example")

        print("printing new /opt/coral_example contents")
        _run_in_shell("ls -la /opt/coral_example")

    print("finished installing coral test model data + scripts")

# installs posenet source code that the students
# modify in S1 to create their camera booth
def _install_posenet_code():
    print("starting install_posenet_code")

    with tempfile.TemporaryDirectory() as temp_dir:
        _run_in_shell(f"git clone --depth=1 '{PROJECT_POSENET_REPO}' project-posenet/", cwd=temp_dir)

        # install requirements (required to actually run it)
        _run_in_shell("./project-posenet/install_requirements.sh", cwd=temp_dir)

        # install into /opt/project-posenet, which is where students are told to find it
        _run_in_shell("sudo rm -rf /opt/project-posenet", cwd=temp_dir)
        _run_in_shell("sudo cp -ra project-posenet /opt/project-posenet", cwd=temp_dir)

    # TODO: list directory contents

    print("finished install_posenet_code")
