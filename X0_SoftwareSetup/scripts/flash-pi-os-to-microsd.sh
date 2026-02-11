#!/usr/bin/env bash

# This should be ran from a host machine (e.g. a desktop computer with
# and SD card reader).

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
sudo partprobe ${micro_sd} # Ensure flashed partitions are visible

# Resize rootfs partition so that it has enough space for PBL source code
sudo parted ${micro_sd} resizepart 2 6GB
sudo e2fsck -f ${micro_sd}2  # Check filesystem (required by resize2fs)
sudo resize2fs ${micro_sd}2  # Resize rootfs filesystem to fill the expanded partition

# Mount bootfs and rootfs filesystems
sudo mkdir ${bootfs} && sudo mount ${micro_sd}1 ${bootfs}
sudo mkdir ${rootfs} && sudo mount ${micro_sd}2 ${rootfs}

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

# Configure dual-mode (gadget-mode) USB driver
sudo bash -c "echo dtoverlay=dwc2 >> ${bootfs}/config.txt"

# Configure ethernet over the dual-mode USB driver
sudo sed -i 's/rootwait/rootwait modules-load=dwc2,g_ether/' ${bootfs}/cmdline.txt

# Configure ssh to be enabled on first boot
sudo touch ${bootfs}/ssh

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

# Make NetworkManager __NOT__ manage the USB connection (it fucking sucks
# and figuring that out costed me two working days).
sudo tee ${rootfs}/etc/NetworkManager/conf.d/usb0-unmanaged.conf <<EOF
[keyfile]
unmanaged-devices=interface-name:usb0
EOF
sudo chmod 600 ${rootfs}/etc/NetworkManager/conf.d/usb0-unmanaged.conf

# Instead, have systemd-networkd manage the USB network connection (it's
# much more reliable: trust me).
sudo tee ${rootfs}/etc/systemd/network/usb0.network <<EOF
[Match]
Name=usb0

[Network]
DHCP=yes
EOF

# Create a oneshot service on first boot to enable systemd-networkd
sudo tee ${rootfs}/etc/systemd/system/firstboot-networkd.service <<'EOF'
[Unit]
Description=Enable systemd-networkd on first boot
ConditionFirstBoot=yes
After=basic.target

[Service]
Type=oneshot
ExecStart=/bin/systemctl enable systemd-networkd
ExecStart=/bin/systemctl start systemd-networkd

[Install]
WantedBy=multi-user.target
EOF
sudo ln -s /etc/systemd/service/firstboot-networkd.service ${rootfs}/etc/systemd/system/multi-user.target.wants/firstboot-networkd.service

# Copy the PBL project to `/opt/PBL` so that all source code is immediately
# available on the Pi (e.g. to reference it, to install the software, etc.)
sudo rsync -av --exclude=".git" --exclude=".idea" ../ ${rootfs}/opt/PBL/
sudo chown -R root:root ${rootfs}/opt/PBL/

# Unmount
sudo umount ${bootfs} && sudo rmdir ${bootfs}
sleep 2
sudo umount ${rootfs} && sudo rmdir ${rootfs}
sync
