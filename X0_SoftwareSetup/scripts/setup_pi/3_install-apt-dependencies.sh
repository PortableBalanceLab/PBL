#!/usr/bin/env bash

set -xeuo pipefail

required_apt_dependencies=(
    "git"                     # Common: for clone-ing examples etc.
    "python3-pip"             # Common: for installing python packages
    "mu-editor"               # Common: recommended to students for editing code
    "thonny"                  # Common: recommended to students for editing code (alternative)
    "realvnc-vnc-server"      # Common: so the Pi can host a VNC interface (#43 #44) (will be replaced with wayvnc in bookworm)

    "curl"                    # S1: for fetching GPG keys
    "wget"                    # S1: for downloading example model/script assets
    "python3-tk"              # S1/L3: used by `guizero` for rendering the GUI
    "libedgetpu1-std"         # S1: to use the Coral USB dongle (requires google apt)
    "python3-tflite-runtime"  # S1: to use the Coral USB dongle (requires google apt)
    "python3-pycoral"         # S1: to use the Coral USB dongle (requires google apt)

    "automake"                # S2/S3: for `autoconf` (building hx711-multi/bcm2835)
    "build-essential"         # S2/S3: ensures there's a C/C++ toolchain available (building hx711-multi/bcm2835)
)

echo "----- starting install apt dependencies -----"
sudo apt install -y ${required_apt_dependencies[@]}
echo "----- finished install apt dependencies -----"
