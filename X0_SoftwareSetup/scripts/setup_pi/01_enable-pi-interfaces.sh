#!/usr/bin/env bash

# This is an optional additional setup script that __must__ be ran
# from the Pi (cannot run this in an emulator - it talks to the kernel
# module API).
#
# These setup steps are normally performed when flashing the Pi (with
# 01_flash-pi-is-to-microsd.sh), but are provided here in case that
# configuration went horribly wrong.

set -xeuo pipefail

required_interfaces=(
    "vnc"     # Common: how users typically access the Pi
    "legacy"  # S1:     for capturing images via the hardware camera ribbon interface
    "i2c"     # S2/S4:  hardware interface used by the sensors
)

needs_reboot=false
echo "----- starting configuring pi interfaces -----"
for interface in "${required_interfaces[@]}"; do
    echo "    enabling ${interface}"
    state_before=$(sudo raspi-config nonint "get_${interface}")
    if [ "${state_before}" -ne 0 ]; then
        echo "    enabling ${interface}"
        sudo raspi-config nonint "do_${interface}" 0
        needs_reboot=true
    else
        echo "    ${interface} is already enabled. Skipping."
    fi
done

if [ "$needs_reboot" = true ]; then
    echo "!!! Hardware changes detected. A reboot is required to apply settings. !!!"
fi
