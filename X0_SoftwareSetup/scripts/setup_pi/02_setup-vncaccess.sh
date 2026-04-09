#!/usr/bin/env bash

# This ensures the `pbl` user can access VNC - even if it isn't
# a `sudo`er.
#
# This is necessary when disabling sudo access for the default
# Pi user because, by default, the VNC server only accepts connections
# from sudo users.

set -xeuo pipefail

# Replace/add authentication line to VNC config
config=/root/.vnc/config.d/vncserver-x11
sudo mkdir -p "$(dirname ${config})"
sudo touch "${config}"
sudo grep -q "^Authentication=" "${config}" && sudo sed -i "s|^Authentication=.*|Authentication=SystemAuth|" "${config}" || echo "Authentication=SystemAuth" | sudo tee -a "${config}"
sudo grep -q "^Permissions=" "${config}" && sudo sed -i "s|^Permissions=.*|Permissions=root:f,%sudo:f,pbl:f|" "${config}" || echo "Permissions=root:f,%sudo:f,pbl:f" | sudo tee -a "${config}"

