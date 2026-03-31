#!/usr/bin/env bash

# This script sets up a host/flashing machine with the necessary
# packages to flash a Pi microSD card from scratch.

set -xeuo pipefail

required_apt_dependencies=(
    "coreutils"          # 01_flash-pi-os-to-microsd.sh
    "xz-utils"           # 01_flash-pi-os-to-microsd.sh
    "parted"             # 01_flash-pi-os-to-microsd.sh
    "mount"              # 01_flash-pi-os-to-microsd.sh
    "e2fsprogs"          # 01_flash-pi-os-to-microsd.sh
    "openssl"            # 01_flash-pi-os-to-microsd.sh
    "rsync"              # 01_flash-pi-os-to-microsd.sh

    "qemu-user-static"   # Emulation: QEMU emulator
    "binfmt-support"     # Emulation: Emulation suppport in Linux
    "systemd-container"  # Emulation: Create root jails with `systemd-nspawn`
)

echo "----- starting install apt dependencies -----"
sudo apt install -y ${required_apt_dependencies[@]}
echo "----- finished install apt dependencies -----"
