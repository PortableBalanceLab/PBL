#!/usr/bin/env bash

set -euo pipefail

usage="usage: $0 SOURCE_IMG_XZ DESTINATION_BLOCK_DEVICE"

if [[ $# -ne 2 ]]; then
    echo "${usage}" 1>&2
    exit 1
fi

image_file=$1
block_device=$2

# Ensure the chosen block device is a USB device, just to reduce the
# chance of accidently flashing the caller's root filesystem or home
# drive (it can happen!)
if ! udevadm info --query property --name "${block_device}" | grep -q '^ID_BUS=usb$'; then
    echo "${block_device}: does not appear to be a USB device - are you SURE it's the microSD card (remove this check if you're sure)"
    exit 1
fi

# Ensure all partitions of the target block device are unmounted
# before flashing the image; otherwise, it can become corrupted
# and unbootable.
sudo umount ${block_device}[0-9] || true

xz -dc "${image_file}" | sudo dd of=${block_device} iflag=fullblock oflag=dsync bs=512K status=progress
sync
