#!/usr/bin/env bash

set -xeuo pipefail

bootfs=/media/adam/boot
rootfs=/media/adam/rootfs

# Hop into a container that runs the Raspberry Pi from the
# host machine (requires package `systemd-container`).
sudo systemd-nspawn \
    -D "${rootfs}" \
    --hostname="raspberrypi" \
    --bind="${bootfs}:/boot" \
    /bin/bash
