#!/usr/bin/env bash

# (make the script fail if any command fails)
set -xeuo pipefail

# these are URLs that the script has to fetch additional data from
#
# ideally, these should all be under `PortableBalanceLab`, so that the
# PBL maintainers can patch it etc. independently of any upstream library
# maintainers
PBL_BCM2835_REPO="https://github.com/PortableBalanceLab/bcm2835"
PBL_PROJECT_POSENET_REPO="https://github.com/PortableBalanceLab/project-posenet"
PBL_ICM20948_REPO="https://github.com/PortableBalanceLab/ICM20948"
PBL_HX711_REPO="https://github.com/PortableBalanceLab/hx711-multi"

# the Raspberry Pi hardware interfaces that should be enabled
PBL_ENABLED_PI_INTERFACES=(
  camera           # S1
  i2c              # S2 and S4
  vnc              # (how students typically access the Pi)
)

# the APT dependencies that should be installed
PBL_APT_DEPS=(
  automake         # for `autoreconf`ing bcm2835 in this script
  git              # for `git clone`ing repositories in this script
  python3-pip      # for `pip install`ing repositories in this script
  python3-tk       # used by GUI packages like guizero
  mu-editor        # recommended to students for editing code
  thonny           # recommended to students as an alternative for editing code
)

# the PIP dependencies that should be installed
PBL_PIP_DEPS=(
  matplotlib                      # all lectures and labs may use this
  numpy                           # L2: recommends this as a useful library and TAs etc. may suggest it during lab sessions
  guizero                         # L3 and S1: used to build GUIs (e.g. camera booths)
  gpiozero                        # L3: used to blink an LED
  pillow                          # S1: for processing images (previously: called `python-imaging` in apt)
  RPi.GPIO                        # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
  spidev                          # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
  smbus                           # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B)) (previously: called `python-smbus` in apt)
  Adafruit-Blinka                 # S4: CircuitPython support
  adafruit-circuitpython-ads1x15  # S4: associated library for the ADS1115 board
)

# downloads+installs bcm2835 on the pi
#
# bcm2835 is used in S2 (IMU). The waveshare guide for SenseHAT
# mentions that it must be installed:
#     - https://www.waveshare.com/wiki/Sense_HAT_(B)
install_bcm2835() {
  echo "----- starting install_bcm2835 -----"
  pushd $(mktemp -d)

  git clone "${PBL_BCM2835_REPO}" bcm2835/
  cd bcm2835/
  autoreconf -f -i  # necessary, because `git` doesn't track timestamps from the original archive
  ./configure
  make
  sudo make check  # sudo required, for some reason
  sudo make install

  popd
  echo "----- finished install_bcm2835 -----"
}

# downloads+installs all TPU runtime coral.ai libraries
# needed to make the neural network camera work (for S1)
#
# pulled from: https://coral.ai/docs/accelerator/get-started
# examples used in S1 are from: https://github.com/google-coral/tflite/tree/master/python/examples/classification
install_coral_dependencies() {
  echo "----- starting install_coral_dependencies -----"

  # install the Edge TPU runtime (USB layer)
  echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt update
  sudo apt install -y libedgetpu1-std python3-pycoral
  sudo pip3 install tflite-runtime

  echo "----- finished install_coral_dependencies ----"
}

# installs extra coral test model data + script that shows
# the students a basic classification example in S1
install_coral_example() {
  # this is based on https://github.com/google-coral/tflite
  # see dir: python/examples/classification
  # contains script: install_requirements.sh

  echo "----- starting install_coral_example (to /opt) -----"

  local base_url=https://github.com/google-coral/edgetpu/raw/master/test_data
  local assets=(
    "mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite"  # hardware tensorflow-lite model
    "mobilenet_v2_1.0_224_inat_bird_quant.tflite"          # software tensorflow-lite model
    "inat_bird_labels.txt"                                 # labels
    "parrot.jpg"                                           # input image
  )

  pushd $(mktemp -d)

  for asset in ${assets[@]}; do
    wget "${base_url}/${asset}"
  done

  # also, download `classify.py` and `classify_image.py` (these are what the students run)
  wget "https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify.py"
  wget "https://raw.githubusercontent.com/google-coral/tflite/eced31ac01e9c2636150decef7d3c335d0feb304/python/examples/classification/classify_image.py"

  # copy data to /opt/coral_example, which is where students are told to find it
  chmod 755 .
  chmod 644 *
  sudo rm -rf /opt/coral_example
  sudo cp -ra . /opt/coral_example

  popd

  echo "----- finished install_coral_example (to /opt) -----"
}

# pre-installs the posenet source code that the students
# modify in S1 to create their camera booth
install_posenet_code() {
  echo "----- starting install_posenet_code -----"
  pushd $(mktemp -d)

  git clone --depth=1 "${PBL_PROJECT_POSENET_REPO}" project-posenet/

  # install requirements (required to actually run it)
  ./project-posenet/install_requirements.sh

  # install into /opt/project-posenet, which is where students are told to find it
  sudo rm -rf /opt/project-posenet
  sudo cp -ra project-posenet /opt/project-posenet

  popd
  echo "----- finished install_posenet_code -----"
}

# installs ICM20948.py, which is used in S2
install_icm20948() {
  echo "----- starting install_icm20948 -----"
  pushd $(mktemp -d)

  git clone "${PBL_ICM20948_REPO}" ICM20948/

  # copy ICM20948.py into /opt so that users can copy it
  # into their home directory during S2
  cd ICM20948/
  chmod 644 ICM20948.py
  sudo cp ICM20948.py /opt/

  popd
  echo "----- finished install_icm20948 -----"
}

# installs hx711-multi library into the python environment
#
# it's used in S3 (ForcePlate) for reading from the ADCs
install_hx711multi() {
  echo "----- starting install_hx711multi -----"
  pushd $(mktemp -d)

  git clone "${PBL_HX711_REPO}" hx711-multi/

  # copy the repo into /opt because S3 mentions running:
  #     /opt/hx711-multi/tests/calibrate.py
  sudo rm -rf /opt/hx711-multi
  sudo cp -ra hx711-multi /opt/hx711-multi

  # and use `pip` to install it as a python package, so that
  # students can just `import hx711_multi.hx711` regardless of
  # where their downstream python script is
  cd hx711-multi/
  pip3 install .

  popd
  echo "----- finished install_hx711multi -----"
}

# installs apt-based (system) dependencies
install_apt_dependencies() {
  echo "----- starting install_apt_dependencies -----"

  sudo apt update
  sudo apt install -y ${PBL_APT_DEPS[@]}

  echo "----- finished install_apt_dependencies -----"
}

# installs python dependencies
install_python_dependencies() {
  echo "----- starting install_python_dependencies -----"

  sudo pip install ${PBL_PIP_DEPS[@]}

  echo "----- finished install_python_dependencies -----"
}

# installs all software dependencies (system and custom stuff)
install_everything() {
  echo "----- starting install_everything -----"

  # install external libraries/applications from package managers
  install_apt_dependencies
  install_python_dependencies

  # install custom PBL-specialized stuff
  install_coral_dependencies  # used in S1
  install_coral_example  # used in S1
  install_posenet_code  # used in S1
  install_bcm2835  # used in S2
  install_icm20948  # used in S2
  install_hx711multi  # used in S3

  echo "----- finished install_everything -----"
}

# configures Pi with VNC, i2c, SPI, etc. support
configure_pi() {
  echo "----- starting configure_pi (VNC, i2c, SPI, etc.) -----"

  set +x
  for ifname in ${PBL_ENABLED_PI_INTERFACES[@]}; do
    config_state_before=$(sudo raspi-config nonint "get_${ifname}")
    sudo raspi-config nonint "do_${ifname}" 0
    config_state_after=$(sudo raspi-config nonint "get_${ifname}")
    echo "enabled ${ifname}: before = ${config_state_before}, after = ${config_state_after}"
  done
  set -x

  echo "----- finished configure_pi (VNC, i2c, SPI, etc.) -----"
}

# this is the part that actually runs something
echo "----- starting setup of Pi for PBL -----"
configure_pi
install_everything
echo "----- finished setup of Pi for PBL: enjoy :> -----"
