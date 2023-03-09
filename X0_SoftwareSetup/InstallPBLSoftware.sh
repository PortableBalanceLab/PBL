#!/usr/bin/env bash

# (make the script fail if any command fails)
set -xeuo pipefail

# the Raspberry Pi interfaces that should be enabled
PBL_ENABLED_PI_INTERFACES=(
  vnc              # recommended interfacing method
  i2c              # some labs need it
  camera           # S1
  spi              # (for good measure: might not be needed)
)

# the APT dependencies that should be installed
PBL_APT_DEPS=(
  git              # for clone-ing things
  mu-editor        # recommended to students for editing code
  thonny           # alternative editor for students
  python3-tk       # used by GUI packages like guizero
  python3-pip      # for installing python packages
)

# the PIP dependencies that should be installed
PBL_PIP_DEPS=(
  numpy            # mentioned in L2 (care: must be installed before scipy)
  matplotlib       # used in various parts of the course
  guizero          # L3 and S1
  gpiozero         # L3?
  RPi.GPIO         # S2 (IMU)
  spidev           # S2 (IMU)
  smbus            # used in S2 (was an apt package called python-smbus)
  pillow           # used in S2 (was an apt package called python-imaging)
  Adafruit-Blinka  # used in S4 (EMG) - provides the CircuitPython support in Python
  adafruit-circuitpython-ads1x15  # used in S4 (EMG) - more specific library that comes with the board (ADS1115)
)

# function: downloads+installs bcm2835 on the pi
#
# the bcm2835 code is used by S2 (IMU)
install_bcm2835() {
  echo "----- install bcm2835 -----"

  pushd $(mktemp -d)
  git clone https://github.com/PortableBalanceLab/bcm2835
  cd bcm2835/
  ./configure
  make
  sudo make check  # sudo required, for some reason
  sudo make install

  popd

  echo "----- /install bcm2835 -----"
}

# function: downloads+installs all TPU runtime coral.ai libraries
# needed to make the neural network camera work (for S1)
#
# pulled from: https://coral.ai/docs/accelerator/get-started
# examples used in S1 are from: https://github.com/google-coral/tflite/tree/master/python/examples/classification
install_coral_dependencies() {
  echo "----- install coral dependencies -----"

  # install the Edge TPU runtime (USB layer)
  echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | sudo tee /etc/apt/sources.list.d/coral-edgetpu.list
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
  sudo apt update
  sudo apt install -y libedgetpu1-std python3-pycoral
  sudo pip3 install tflite-runtime

  echo "----- /install coral dependencies ----"
}

# function: installs extra coral test model data + script
# that shows the students a basic classification example in S1
install_coral_example() {
  # this is based on https://github.com/google-coral/tflite
  # see dir: python/examples/classification
  # contains script: install_requirements.sh

  echo "----- install /opt/coral_example -----"

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

  echo "----- /install /opt/coral_example -----"
}

# function: pre-installs the posenet source code that the students
# modify in S1 to create their camera booth
install_posenet_code() {
  echo "----- install /opt/project-posenet -----"
  pushd $(mktemp -d)

  git clone --depth=1 https://github.com/google-coral/project-posenet.git

  # install requirements (required to actually run it)
  ./project-posenet/install_requirements.sh

  # install into /opt/project-posenet, which is where students are told to find it
  sudo rm -rf /opt/project-posenet
  sudo cp -ra project-posenet /opt/project-posenet

  popd
  echo "----- /install /opt/project-posenet -----"
}

# function: installs ICM20948.py, which is used in S2
install_icm20948() {
  echo "----- install ICM20948.py to /opt -----"
  pushd $(mktemp -d)
  wget "https://gist.githubusercontent.com/adamkewley/092b8e5c3594f30bad91f1cb6527b78b/raw/cbc6ac89302d3288af810660ef5dabd3990e3f47/ICM20948.py"
  chmod 644 ICM20948.py
  sudo cp ICM20948.py /opt/
  popd
  echo "----- /install ICM20948.py to /opt -----"
}

# function: installs hx711-multi library into the python
# environment
install_hx711multi() {
  echo "----- install hx711-multi -----"
  pushd $(mktemp -d)

  git clone https://github.com/PortableBalanceLab/hx711-multi.git
  cd hx711-multi/
  pip3 install .

  popd
  echo "----- /install hx711-multi -----"
}


# (end of _declarations_: time to run stuff ;))


echo "----- starting pi configuration/installation -----"

# configure the pi (VNC, i2c, etc.)
for ifname in ${PBL_ENABLED_PI_INTERFACES[@]}; do
  config_state_before=$(sudo raspi-config nonint "get_${ifname}")
  sudo raspi-config nonint "do_${ifname}" 0
  config_state_after=$(sudo raspi-config nonint "get_${ifname}")
  echo "enabled ${ifname}: before = ${config_state_before}, after = ${config_state_after}"
done

echo "----- installing system (APT) packages -----"
sudo apt update
sudo apt install -y ${PBL_APT_DEPS[@]}

echo "----- installing python (PIP) packages -----"
sudo pip install ${PBL_PIP_DEPS[@]}

echo "----- installing specialized/lab-specific libraries/code -----"

install_coral_dependencies  # used in S1
install_coral_example  # used in S1
install_posenet_code  # used in S1
install_bcm2835  # used in S2
install_icm20948  # used in S2
install_hx711multi  # used in S3

echo "----- finished pi configuration/installation -----"
