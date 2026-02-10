#!/usr/bin/env bash

# This should be ran from a host machine (e.g. a desktop computer with
# and SD card reader).

set -xeuo pipefail

micro_sd=/dev/sdb
mnt=/media/adam
bootfs=${mnt}/bootfs
rootfs=${mnt}/rootfs
base_user=pbl
base_password=thebasecase

# Ensure existing filesystem is unmounted
if [[ -e ${bootfs} ]]; then sudo umount ${bootfs}; fi
if [[ -e ${rootfs} ]]; then sudo umount ${rootfs}; fi

# Flash image to microSD card
xz -dc ~/Downloads/2022-09-22-raspios-bullseye-armhf.img.xz | sudo dd of=${micro_sd} iflag=fullblock oflag=dsync bs=512K status=progress
sudo sync
sudo partprobe ${micro_sd} # Ensure flashed partitions are visible

# Resize rootfs partition so that it has enough space for PBL
sudo parted ${micro_sd} resizepart 2 6GB
# Resize rootfs filesystem to fill the expanded partition
sudo e2fsck -f ${micro_sd}2
sudo resize2fs ${micro_sd}2

# Mount bootfs and rootfs filesystems
sudo mkdir ${bootfs} && sudo mount ${micro_sd}1 ${bootfs}
sudo mkdir ${rootfs} && sudo mount ${micro_sd}2 ${rootfs}

# Configure dual-mode (gadget-mode) USB driver
sudo bash -c "echo dtoverlay=dwc2 >> ${bootfs}/config.txt"

# Configure ethernet over the dual-mode USB driver
sudo sed -i 's/rootwait/rootwait modules-load=dwc2,g_ether/' ${bootfs}/cmdline.txt

# Enable ssh
sudo touch ${bootfs}/ssh

# Configure root user
hashed_password=$(echo "${base_password}" | openssl passwd -6 -stdin)
echo "pw == ${base_password}, hash = ${hashed_password}"
echo "${base_user}:${hashed_password}" | sudo tee ${bootfs}/userconf.txt

# Note: copying any SSH keys etc. and individualization comes after configuring
# the software.

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
sudo rsync -av --exclude=".git" ../ ${rootfs}/opt/PBL/
sudo chown -R root:root ${rootfs}/opt/PBL/

# Unmount
sudo umount ${bootfs} && sudo rmdir ${bootfs}
sleep 2
sudo umount ${rootfs} && sudo rmdir ${rootfs}
