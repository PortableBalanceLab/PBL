#!/usr/bin/env bash

rootfs_mountpoint=/media/adam/rootfs

# Get QEMU and ensure host kernel has binfmt support (so it can load
# other architectures' binaries).
sudo apt-get install qemu-user-static binfmt-support

# Copy QEMU into the Raspberry Pi's root filesystem
sudo cp -a /usr/bin/qemu-armhf-static ${rootfs_mountpoint}/usr/bin/

# Bind host kernel's devfs, procfs, sysfs, etc. into the Pi's root filesystem
for dir in /dev /proc /sys /run; do sudo mount --bind $dir ${rootfs_mountpoint}${dir}; done

# Chroot into the Pi's root filesystem - effectively, emulate it being the operating system root
sudo chroot ${rootfs_mountpoint} /bin/bash

# !! Do stuff as-if on the Pi !!

# After: unbind forwarded filesystems
for dir in /dev /proc /sys /run; do echo "unmounting ${rootfs_mountpoint}${dir}" && sudo umount ${rootfs_mountpoint}${dir} && sleep 1; done
