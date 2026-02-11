#!/usr/bin/env bash

required_pip_dependencies=(
    "matplotlib"                      # Common: suggested in L2 and used by many lectures/practicals
    "numpy"                           # Common: suggested in L2 and may be recommended by TAs etc.
    "numpy"                           # L2: recommended to students in the lecture notes
    "matplotlib"                      # L2: recommended to students in the lecture notes
    "guizero"                         # L3: used to build GUIs in the lecture
    "gpiozero"                        # L3: used to blink and LED in the lecture
    "guizero"                         # S1: used to build camera booth GUI
    "pillow"                          # S1: used for processing images (previously: called `python-imaging` in apt)
    "svgwrite"                        # S1: transitive dependency for project-posenet
    "RPi.GPIO"                        # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "spidev"                          # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B))
    "smbus"                           # S2: dependency from SenseHAT (https://www.waveshare.com/wiki/Sense_HAT_(B)) (previously: called `python-smbus` in apt)
    "Adafruit-Blinka"                 # S4: CircuitPython support
    "adafruit-circuitpython-ads1x15"  # S4: library for the ADS1115 board
)

echo "----- starting install pip dependencies -----"
sudo pip install ${required_pip_dependencies[@]}
echo "----- finished install pip dependencies -----"
