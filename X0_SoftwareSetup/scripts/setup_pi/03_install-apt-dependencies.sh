#!/usr/bin/env bash

set -xeuo pipefail

required_apt_dependencies=(
    "build-essential"             # Common:  ensures there's a C/C++ toolchain available (can be handy when building native Python wheels etc.)
    "curl"                        # S1:      for fetching GPG keys
    "gir1.2-gtk-3.0"              # S1:      transitive dependency for project-posenet
    "git"                         # Common:  for clone-ing examples etc.
    "gobject-introspection"       # S1:      transitive dependency for project-posenet
    "gstreamer1.0-plugins-bad"    # S1:      transitive dependency for project-posenet
    "gstreamer1.0-plugins-good"   # S1:      transitive dependency for project-posenet
    "libedgetpu1-std"             # S1:      to use the Coral USB dongle (requires google apt)
    "mu-editor"                   # Common:  recommended to students for editing code
    "neovim"                      # Common:  recommended for 1337 h4x0rs
    "python3-gi"                  # S1:      transitive dependency for project-posenet
    "python3-gst-1.0"             # S1:      transitive dependency for project-posenet
    "python3-numpy"               # S1:      transitive dependency for project-posenet
    "python3-pil"                 # S1:      used for processing images (previously: called `python-imaging` in apt)
    "python3-pip"                 # Common:  for installing python packages
    "python3-pycoral"             # S1:      to use the Coral USB dongle (requires google apt)
    "python3-rpi.gpio"            # S1:      transitive dependency for project-posenet
    "python3-smbus"               # S2:      dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B)) (previously: called `python-smbus` in apt)
    "python3-tflite-runtime"      # S1:      to use the Coral USB dongle (requires google apt)
    "python3-tk"                  # L3 & S1: used by `guizero` (e.g. to create the booth ui)
    "realvnc-vnc-server"          # Common:  so the Pi can host a VNC interface (#43 #44) (will be replaced with wayvnc in bookworm)
    "thonny"                      # Common:  recommended to students for editing code (alternative)
    "wget"                        # S1:      for downloading example model/script assets
)

echo "----- starting install apt dependencies -----"
sudo apt update
sudo apt install -y ${required_apt_dependencies[@]}
echo "----- finished install apt dependencies -----"
