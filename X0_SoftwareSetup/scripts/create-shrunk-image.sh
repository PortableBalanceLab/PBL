#!/usr/bin/env bash

# This script creates a shrunk Pi image from the contents
# of the given block device (micro_sd)

set -xeuo pipefail

micro_sd=/dev/sdf
mnt=/media/adam
bootfs=${mnt}/boot
rootfs=${mnt}/rootfs
raw_img_output=/home/adam/Desktop/PBL.img
shrunk_img_output=/home/adam/Desktop/PBL_shrunk.img.xz

# Ensure the user running this script is root (required)
if [[ $EUID -ne 0 ]]; then
    echo "This script must be ran with sudo or as root."
    exit 1
fi

# Ensure the chosen block device is a USB device, just to reduce the
# chance of accidently flashing the caller's root filesystem or home
# drive (it can happen!)
if ! udevadm info --query property --name "${micro_sd}" | grep -q '^ID_BUS=usb$'; then
    echo "${micro_sd}: does not appear to be a USB device - are you SURE it's the microSD card (remove this check if you're sure)"
    exit 1
fi

# Ensure the chosen block device isn't massive. If it's >100 GB then
# there's a chance the caller has accidently specified a large USB
# hard drive or something
micro_sd_size=$(lsblk "${micro_sd}" --bytes --nodeps --noheadings --output SIZE)
if [[ ${micro_sd_size} -gt 100000000000 ]]; then
    echo "${micro_sd}: seems very big - are you SURE it's the microSD card (remove this check if you're sure)"
    exit 1
fi

# Ensure existing filesystem is unmounted (just so we have
# a known initial state).
umount -l "${bootfs}" || true
umount -l "${rootfs}" || true

# Ensure the mount points are cleared (just so we have a known
# initial state).
if [[ -d "${bootfs}" ]]; then rmdir "${bootfs}"; fi
if [[ -d "${rootfs}" ]]; then rmdir "${rootfs}"; fi

# Mount the root filesystem.
mkdir "${rootfs}" && mount "${micro_sd}2" "${rootfs}"

# Create a zeroed `wipefile` on the root filesystem that fills all
# available space on the Pi's root partition (compressibility)
dd if=/dev/zero of="${rootfs}/wipefile" oflag=dsync bs=512K status=progress || true

# Remove `wipefile` (it has done its job of zeroing the unused space)
rm "${rootfs}/wipefile"

# Unmount Pi's root filesystem
umount "${rootfs}"

# Create raw disk image
dd if="${micro_sd}" of="${raw_img_output}" bs=4M status=progress

# Shrink the image with PiShrink
./PiShrink/pishrink.sh -v -n -Z "${raw_img_output}" "${shrunk_img_output}"
