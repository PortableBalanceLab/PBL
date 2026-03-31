#!/usr/bin/env bash

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

echo "----- finished configuring pi interfaces -----"
