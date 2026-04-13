#!/usr/bin/env bash

set -xeuo pipefail

required_pip_dependencies=(
    "adafruit-blinka==8.64.0"                # S4:      CircuitPython support
    "adafruit-circuitpython-ads1x15==3.0.3"  # S4:      library for the ADS1115 board
    "guizero==1.1.1"                         # L3 & S1: used to build GUIs in the lecture
    "matplotlib==3.3.4"                      # Common:  suggested in L2 and used by many lectures/practicals
    "spidev==3.5"                            # S2:      dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "svgwrite==1.4.3"                        # S1:      transitive dependency for project-posenet
)

echo "----- starting install pip dependencies -----"
sudo pip install "${required_pip_dependencies[@]}"
echo "----- finished install pip dependencies -----"
