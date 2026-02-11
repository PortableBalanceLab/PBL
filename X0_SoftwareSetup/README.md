# `X0`: Extra Content 0: Software Setup

> ℹ️ **Note**: If you're a student on the course, then you probably don't need to **do** anything
> on this page. The organizers have probably already installed the necessary software for you. This 
> page is provided for your information.

This guide sets up a Raspberry Pi (Zero or 4) from scratch such that it's ready for use in the course.

## Hardware Prerequisites

- A Linux computer with a Micro SD card reader. This "host" computer runs `flash-pi-os-to-microsd.sh` script. If
  you don't have a Linux computer handy, you can use a spare Raspberry Pi flashed with a base
  Raspbian image. You can install the base image using the Raspberry Pi imager, https://www.raspberrypi.com/software/,
  which you should be able to install onto your Windows/macOS laptop - it will yield a Linux computer (a Pi).
- An Raspbian OS image. Specifically, `2022-09-22-raspios-bullseye-armhf.img.xz` which is verified
  to work with PBL's hardware. Get it from https://downloads.raspberrypi.com/raspios_armhf/images/raspios_armhf-2022-09-26/
- A way of running stuff on the Pi after it's flashed:
  - `flash-pi-os-to-microsd.sh` enables LAN-over-USB. After flashing, you can put the microSD
    card into a Raspberry Pi and then use a USB cable from your computer to the Pi to create a network
    connection. Always plug Micro-USB cords into the USB slot on Pi Zeros. You must also tell your OS to
    "share my internet connection through this adaptor" after it recognizes the USB device as an ethernet
    adaptor.
  - You can also just connect a mouse+keyboard+monitor to the Pi and manually configure it to join
    a network. Use a local WiFi hotspot if necessary.
  - However you connect to the Pi, it must have an internet connection in order to install software
    onto the flashed image.


## Organizational Prerequisites

### Create a Spreadsheet for Tracking Pi Credentials/Information

Use whatever organizational method you prefer (e.g. google doc). The spreadsheet
should have the following columns:

- `ID`: unique physical ID that was written on the Pi (e.g. `AA`)
- `SSID`: WiFi SSID that the Pi will automatically join on power-on (e.g. `TUD-Facility`)
- `WiFi Password`: password for the WiFi network identified by `SSID` (e.g. `sometringfromTUDfacilitywebsite`)
- `hostname`: unique virtual hostname for this Pi (e.g. `pblhostaa`)
- `password`: password for the `pbl` account (e.g. `monkey99`)
- `MAC`: physical MAC address of the Pi (e.g. `9c:6b:00:b0:f5:e5`)

The reason this information is collected is purely administrative:
- `ID` links one Pi to the other information (e.g. if a group loses their password but
  knows their `ID` it can be fixed).
- `SSID` is necessary when different Pis use different hotspots (e.g. local hotspots).
- `WiFi Password` is necessary if local hotspots need to be individualized
- `hostname` is necessary because networking portals use it when listing devices
- `password` is necessary so that students can't as easily accidently connect to other groups' Pis
- `MAC` is necessary to register the device on networks that require MAC addresses (e.g. `TUD-facilty`)


### Physically ID the Pi

- Use a permanent marker to physically write an ID onto the Pi. Single letters are simplest.
- Write the same ID on the SD card, so that the software configuration (e.g. password, hostname)
  can be tied to the physical system (e.g. MAC address).
- **Add the `ID` to the spreadsheet**. The ID is useful to have in case Pis are mixed up, or for cross-checking with
  other information.


## Step 1: Sanity Check: We Might Already Have a Base Image

**Before you start going through an arduous flashing/configuration process, ask whether there's a
base image lying around somewhere. They're usually over-provisioned for the course.**

Usually, after the first (base) image has been flashed + configured with the scripts, the resulting
configured system will be cloned into a new image binary. The configured base image is then usually
just cloned onto all other Pis and then individualized (unique password, unique hostname) later on.

**If you have an existing base image, then you can skip steps 2 and 3** and just `dd` the base image to
a microSD card. If you need to do this *a lot* (e.g. you're a course organizer), use a hardware
microSD duplicator that can do many in parallel.


## Step 2: Flash the Pi's microSD Card

This step flashes a Raspbian OS image onto a microSD card and then pre-configures the OS
known credentials, LAN-over-USB, and copies the top-level PBL directory onto the Pi so that
it doesn't have to be separately downloaded.

- All the following steps should be conducted from a Linux host machine. The host machine
  doesn't need to be a Raspberry Pi (e.g. I do it from an AMD desktop computer with Ubuntu 24).
- Plug the microSD card into your microSD card reader and note down its device assignment
  and mount point. You can use `lsblk` to do this. For example, in my case, my micro SD card
  reader mounts `/dev/sdb` to `/media/adam` (if there's something on it).
- **Carefully read** `scripts/flash-pi-os-to-microsd.sh` and edit it according to how your
  computer mounts things. **BEWARE**: IT'S EXTREMELY DANGEROUS IF YOU SCREW THIS UP AND
  ACCIDENTLY GIVE IT YOUR ROOT FILESYSTEM - IT WILL NUKE YOUR COMPUTER. YOU WILL CRY.
- Once you're confident that the script is safe to run, run it. It will take a few minutes
  to flash and program the microSD card.
- Once the card is flashed, you can safely remove the card.


## Step 3: Configure the base image

This step boots up the Raspbian OS image on a lab Raspberry Pi and then configures it with
the necessary PBL-specific software. The `flash-pi-os-to-microsd.sh` script in step 2 doesn't
do this because some steps require booting the OS.

- Put the flashed microSD card from step 2 into a Raspberry Pi. I typically put it into a
  Raspberry Pi zero (minimum spec) to do this.
- Connect to the Pi (explained in prerequisites above) either via SSH or physically - you need
  a working terminal in the Pi. 
- Go through the following steps in the terminal:

```bash
#!/usr/bin/env bash

# Change into the PBL/ directory that was installed
# by the `flash-pi-os-to-microsd.sh` script.
cd /opt/PBL/X0_SoftwareSetup/

# Install dependencies and `pbl`
./scripts/setup_pi.sh
```

## Step 4: Validate and Clone the Base Image (if desired)

After completing step 3, the microSD card is fully configured, but not yet individualized
(unique password/hostname). This is the best time to verify that the distribution behaves
as expected and freeze it for mass cloning.

```bash
#!/usr/bin/env bash

# E.g. to validate the install, run the `pbl` test suite - all tests should pass
pbl test

# ... but also remember to do some manual/exploratory testing...
```

### Cloning Method: Hardware microSD Duplicator

Hardware duplicators are available for purchase. E.g. EZ DUPE 1 on 15, UReach microSD
Duplicator tower 1-23. Robotics departments in TU Delft might already own something
like these. Check with groups that need to flash many robots (e.g. drone research).

Hardware duplicators are by far the fastest way to bulk-copy microSD cards: they're also
the most expensive :wink:, so it's best to try and find one that's already purchased and
beg a little.

### Cloning Method: `rpi-clone`

This performs a filesystem-level clone from one Pi to an SD card reader. Because it copies
files, rather than blindly copying blocks, it is usually faster than `dd`, but it requires
a Pi host.

- Get `https://github.com/billw2/rpi-clone` (e.g. `cd $(mktemp -d) && git clone https://github.com/billw2/rpi-clone`)
- Install it with `cp rpi-clone rpi-clone-setup /usr/local/sbin`
- Put the SD card into the SD card reader
- See if it's mounted with `sudo lsblk`
- Unmount it with `sudo umount /media/pbl/*`
- Clone with `sudo rpi-clone -s HOSTNAME -v -f sda`
- Unmount
- Plug into "slave" pi
- Ssh into the pi
- Change password with `passwd`

### Cloning Method: `dd`

This performs a block-level clone of a microSD card, which will copy all data on the card -
including any junk that isn't actually part of the filesystem. Therefore, it's slower than
copying the file (inodes), but can be done from any macOS/Linux machine and guarantees a
byte-level clone.

## Step 5: Individualize a microSD Card to a Pi

This step individualizes the image, which makes it unique for a particular group/box.
Therefore, this process should be repeated for all boxes.

All microSD cards are essentially identical to each other - apart from their hostname and
password. The hostname is important because institutional networks tend to use it when
listing devices connected to networks (e.g. `TUD-Facility` portal does this). The password
is important because it reduces the chance of a student connecting to another group's Pi
by accident.

To individualize a Pi, use the `individualize-pi.sh` script that's installed on the Pi
during flashing:

```bash
#!/usr/bin/env bash

# Change into the PBL/ directory that was installed
# by the `flash-pi-os-to-microsd.sh` script.
cd /opt/PBL/X0_SoftwareSetup/

# Switch to root account (requires root password)
su -

# Call the script, providing the new username/password
./scripts/individualize-pi.sh new_hostname new_password

# Note: `sudo` is now disabled for this Pi. From now on, you need to
# `su -` to the `root` account to modify the Pi.

# Note: also, make sure to note down the Pi's WiFi adaptor MAC address
ip link show wlan0 | grep -Po 'ether \K[^ ]*'
```

**Add the `new_hostname`, `new_password`, and MAC address to the organizational spreadsheet**.
