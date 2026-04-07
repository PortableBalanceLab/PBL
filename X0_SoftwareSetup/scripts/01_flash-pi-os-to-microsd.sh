#!/usr/bin/env bash

# This script flashes a microSD card with the necessary Raspberry Pi OS,
# configuration, and software for the PortableBalanceLab course.
#
# It should be ran from a host/flashing machine, which is assumed to be
# a Linux desktop computer with an SD card reader. You should read the
# variables below and ensure they're correct for your machine!

set -xeuo pipefail

# Note: the version of Raspbian matters _a lot_ because some of the
# hardware (primary, the CoralAI dongle) isn't supported on newer
# OSes.
#
# This one is from: https://downloads.raspberrypi.com/raspios_armhf/images/raspios_armhf-2022-09-26/2022-09-22-raspios-bullseye-armhf.img.xz
raspbian_img=~/Downloads/2022-09-22-raspios-bullseye-armhf.img.xz
micro_sd=/dev/sdb
mnt=/media/adam
bootfs=${mnt}/boot
rootfs=${mnt}/rootfs
base_user=pbl
base_password=thebasecase
root_password=therootcause

# Ensure the chosen block device isn't massive. If it's >100 GB then
# there's a chance the caller has accidently specified their SSD or
# something
micro_sd_size=$(lsblk "${micro_sd}" --bytes --nodeps --noheadings --output SIZE)
if [[ ${micro_sd_size} -gt 100000000000 ]]; then
    echo "${micro_sd}: seems very big - are you SURE it's the microSD card (remove this check if you're sure)"
    exit 1
fi

# Ensure existing filesystem is unmounted
sudo umount --quiet ${micro_sd}1 || true
sudo umount --quiet ${micro_sd}2 || true

# Ensure mount points are cleared (they're remade after)
if [[ -d "${bootfs}" ]]; then sudo rmdir "${bootfs}"; fi
if [[ -d "${rootfs}" ]]; then sudo rmdir "${rootfs}"; fi

# Flash image to microSD card
#
# Note: the block size and syncing flags are important to reduce
# microSD flakiness issues.
xz -dc ${raspbian_img} | sudo dd of=${micro_sd} iflag=fullblock oflag=dsync bs=512K status=progress
sudo sync
sudo partprobe "${micro_sd}"  # Ensure flashed partitions are visible

# Resize rootfs partition so that it has enough space for PBL source code
sudo parted "${micro_sd}" resizepart 2 6GB
sudo e2fsck -f "${micro_sd}2"  # Check filesystem (required by resize2fs)
sudo resize2fs "${micro_sd}2"  # Resize rootfs filesystem to fill the expanded partition

# Mount bootfs and rootfs filesystems
sudo mkdir "${bootfs}" && sudo mount "${micro_sd}1" "${bootfs}"
sudo mkdir "${rootfs}" && sudo mount "${micro_sd}2" "${rootfs}"

# Sanity-check that the boot files aren't empty
#
# This is necessary because mis-mounted microSD filesystems can sometimes
# contain files that exist (by name) but are empty.
if [[ ! -s "${bootfs}/config.txt" ]]; then
    echo "${bootfs}/config.txt: is missing or empty, has the boot drive been mounted correctly?" 1>&2
    exit 1
fi
if [[ ! -s "${bootfs}/cmdline.txt" ]]; then
    echo "${bootfs}/cmdline.txt: is missing or empty, has the boot drive been mounted correctly?" 1>&2
    exit 1
fi

# Configure UART (serial, GPIO) connection support
echo "enable_uart=1" | sudo tee -a "${bootfs}/config.txt"

# Configure ssh to be enabled on first boot
sudo touch "${bootfs}/ssh"

# Configure vnc to be enabled on first boot
sudo touch "${bootfs}/vnc"

# Enable camera (ribbon, spi) interface and kernel module on first boot (S1)
#
# This is equivalent to running `sudo raspi-config nonint do_legacy 0`
sudo sed -i 's/^start_x=0/start_x=1/' "${bootfs}/config.txt" || echo "start_x=1" | sudo tee -a "${bootfs}/config.txt"
echo "gpu_mem=64" | sudo tee -a "${bootfs}/config.txt"
if ! grep -q "bcm2835-v4l2" "${rootfs}/etc/modules"; then
    echo "bcm2835-v4l2" | sudo tee -a "${rootfs}/etc/modules"
fi

# Enable i2c hardware interface on boot (S2/S4)
#
# This is equivalent to running `sudo raspi-config nonint do_i2c 0` (see `enable-pi-drivers.sh`)
echo "dtparam=i2c_arm=on" | sudo tee -a "${bootfs}/config.txt"
echo "i2c-dev" | sudo tee -a "${rootfs}/etc/modules"

# Configure base user
#
# The base user is what the students use. It should ideally be non-sudo so
# that students are less likely to brick their Raspberry Pi.
hashed_base_password=$(echo "${base_password}" | openssl passwd -6 -stdin)
echo "pw == ${base_password}, hash = ${hashed_base_password}"
echo "${base_user}:${hashed_base_password}" | sudo tee ${bootfs}/userconf.txt

# Configure root user
#
# The root user is what the administrators may use to configure the device. It
# is the same for all devices, but shouldn't be shared around.
#
# Note: the root user can't directly SSH onto the device. You must first SSH
# as the base user and then `su` to root. This is to prevent everyone having
# SSH access to everyone else's Pi.
hashed_root_password=$(echo "${root_password}" | openssl passwd -6 -stdin)
echo "root pw == ${root_password}, hash = ${hashed_root_password}"
sudo sed -i "s|^root:[^:]*|root:${hashed_root_password}|" ${rootfs}/etc/shadow

# Configure TUD-Facility WiFi Network
#
# This is the default WiFi network that the Pi will try to join when it's turned
# on. NOTE: it may not be able to connect straight away, because TUD-Facility
# requires that the Raspberry Pi's MAC address has been registered with the
# network via https://infra-ict.tudelft.nl/portal/labs/list_labs.php
sudo tee "${bootfs}/wpa_supplicant.conf" <<EOF
country=NL
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="TUD-facility"
    psk="0b62dc191344e"
}
EOF

# Copy the PBL project to `/opt/PBL` so that all source code is immediately
# available on the Pi (e.g. to reference it, to install the software, etc.)
sudo rsync -av --exclude=".git" --exclude=".idea" ../ "${rootfs}/opt/PBL/"
sudo chown -R root:root "${rootfs}/opt/PBL/"

# Copy `qemu-armhf-static` into the root filesystem so that QEMU-based emulators
# can boot into the Raspberry Pi.
sudo cp -a "/usr/bin/qemu-armhf-static" "${rootfs}/usr/bin/"

# Use a container + QEMU emulator to hop into the Raspberry Pi's filesystem and
# then run the Pi's setup scripts.
sudo systemd-nspawn \
    -D "${rootfs}" \
    --hostname="raspberrypi" \
    --bind="${bootfs}:/boot" \
    /bin/bash -c "cd /opt/PBL/X0_SoftwareSetup && ./scripts/02_setup_pi.sh"

# Flashing complete - unmount flashed partitions
sudo umount -l "${bootfs}" && sudo rmdir "${bootfs}"
sudo umount -l "${rootfs}" && sudo rmdir "${rootfs}"
sync
