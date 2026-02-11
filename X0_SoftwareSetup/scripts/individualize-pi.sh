#!/usr/bin/env bash

# This script individualizes the Pi for a particular box/group

base_username=pbl
old_hostname=$(hostname)
new_hostname=pblhostc
new_password=monkeymagic

if [[ "$(id -u)" -ne 0 ]]; then
    echo "This script must be ran as root"
    exit 1
fi

# Update hostname
hostnamectl set-hostname "${hostname}"
sed -i 's/${old_hostname}.*/${new_hostname}/' /etc/hosts

# Update password
echo "${username}:${new_password}" | chpasswd

# Disable sudo access for the base user.
#
# From this point on, configuration requires explicitly switching to the
# `root` user, which has a fixed (but not shared) password on all Pis.
#
# This step helps protect the students from bricking the Pi. Almost every
# year, 1-2 groups brick their Pi by copy+pasting some `sudo` command from
# ChatGPT.
deluser "${username}" sudo
sed -i "/^${username}/d" /etc/sudoers
rm /etc/sudoers.d/010_pi-nopasswd
