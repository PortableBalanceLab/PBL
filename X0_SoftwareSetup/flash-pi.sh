#!/usr/bin/env bash

set -xeuo pipefail

micro_sd=/dev/sdb
mnt=/media/adam
bootfs=${mnt}/bootfs
rootfs=${mnt}/rootfs
base_user=pbl
base_password=thebasecase

# Flash image to MicroSD
xz -dc ~/Downloads/2025-12-04-raspios-trixie-armhf.img.xz | sudo dd of=${micro_sd} iflag=fullblock oflag=dsync bs=512K status=progress
sudo sync
sudo partprobe ${micro_sd} # Ensure flashed partitions are visible

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

# Copying the SSH key comes after first login (MAC, password, hostname, etc.)

# Make NetworkManager __NOT__ manage the USB connection (it fucking sucks
# and figuring that out costed me two working days).
sudo tee ${rootfs}/etc/NetworkManager/conf.d/usb0-unmanaged.conf <<EOF
[keyfile]
unmanaged-devices=interface-name:usb0
EOF
sudo chmod 600 ${rootfs}/etc/NetworkManager/conf.d/usb0-unmanaged.conf

# Instead, use systemd-networkd
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

# Unmount
sudo umount ${bootfs} && sudo rmdir ${bootfs}
sleep 2
sudo umount ${rootfs} && sudo rmdir ${rootfs}

