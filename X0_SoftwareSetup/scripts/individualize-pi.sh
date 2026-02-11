#!/usr/bin/env bash

# This script individualizes the Pi for a particular box/group

set -xeuo pipefail

if [[ "$(id -u)" -ne 0 ]]; then
    echo "This script must be ran as root"
    exit 1
fi

if [[ $# -ne 2 ]]; then
   echo "Usage: $0 NEW_HOSTNAME NEW_PASSWORD" >&2
   exit 1
fi

old_hostname=$(hostname)
new_hostname=$1
username=pbl
new_password=$2

# Update hostname
hostnamectl set-hostname "${new_hostname}"
sed -i 's/${old_hostname}.*/${new_hostname}/g' /etc/hosts
echo "Hostname changed: '${old_hostname}' --> '${new_hostname}'"

# Update password
echo "${username}:${new_password}" | chpasswd
echo "Password changed"

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
echo "Sudo access was revoked for ${username}"

wifi_mac_address=$(ip link show wlan0 | grep -Po 'ether \K[^ ]*')

# Print information banner, so that the admin knows what's up
# and knows what to do next.

set +x

echo "------------------------------------------------------"
echo "             Individualization Complete               "
echo "------------------------------------------------------"
echo "Device details (you probably should write these down):"
echo "                                                      "
echo "    hostname    = ${new_hostname}                     "
echo "    password    = ${new_password}                     "
echo "    MAC address = ${wifi_mac_address}                 "
echo "                                                      "
echo "Note: some changes, such as the hostname and sudo,    "
echo "      access, won't take effect until you restart.    "
echo "Note #2: you may also want to note down the ID, WiFi  "
echo "         SSID, and WiFi password of the Pi, if you    "
echo "         know them.                                   "

