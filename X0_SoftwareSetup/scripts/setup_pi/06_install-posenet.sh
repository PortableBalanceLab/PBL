#!/usr/bin/env bash

set -xeuo pipefail

echo "----- installing posenet requirements -----"
# Add v4l2 video module to kernel
if ! grep -q "bcm2835-v4l2" /etc/modules; then
  echo bcm2835-v4l2 | sudo tee -a /etc/modules
fi
sudo modprobe bcm2835-v4l2
# old approach: this has now been rolled into apt/pip install
# sudo ./project-posenet/install_requirements.sh
echo "----- finished installing posenet requirements -----"

echo "----- copying project-posenet to /opt/project-posenet/ -----"
sudo rm -rf /opt/project-posenet
sudo cp -ra ./project-posenet/ /opt/project-posenet
echo "----- finished copying project-posenet to /opt/project-posenet/"

# Print project-posenet directory (debugging)
ls -la /opt/project-posenet
