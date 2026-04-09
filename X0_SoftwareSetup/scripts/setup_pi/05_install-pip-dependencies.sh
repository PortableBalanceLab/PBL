#!/usr/bin/env bash

set -xeuo pipefail

required_pip_dependencies=(
    "Adafruit-Blinka"                 # S4:      CircuitPython support
    "adafruit-circuitpython-ads1x15"  # S4:      library for the ADS1115 board
    "guizero"                         # L3 & S1: used to build GUIs in the lecture
    "matplotlib"                      # Common:  suggested in L2 and used by many lectures/practicals
    "spidev"                          # S2:      dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "svgwrite"                        # S1:      transitive dependency for project-posenet
)

echo "----- starting install pip dependencies -----"
sudo pip install "${required_pip_dependencies[@]}"
echo "----- finished install pip dependencies -----"
