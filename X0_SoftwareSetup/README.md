# `X0`: Extra Content 0: Software Setup

> ℹ️ **Note**: If you're a student on the course, then you probably don't need to **do** anything
> on this page. The organizers have probably already installed the necessary software for you. This 
> page is provided for your information.

This guide sets up a Raspberry Pi (Zero or 4) from scratch such that it's ready for use in the course.

## Hardware Prerequisites

- A Linux computer with a Micro SD card reader, to run the `flash-pi-os-to-microsd.sh` script. If
  you don't have a Linux computer handy, you can use a spare Raspberry Pi flashed with a base
  Raspbian image. You can install the base image using the Raspberry Pi imager, https://www.raspberrypi.com/software/,
  which you should be able to install onto your Windows/macOS laptop.
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


## Step 1: Make Sure There Isn't a Base Image Lying Around Somewhere Already

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

- All the following steps should be conducted from a Linux host machine. It doesn't need
  to be a Raspberry Pi (e.g. I do it from an AMD desktop computer with Ubuntu 24).
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

# Change into the PBL/ directory installed by flash-pi-os-to-microsd.sh
cd /opt/PBL/X0_SoftwareSetup/

# Install dependencies and `pbl`
./scripts/setup_pi.sh

# Run `pbl` test suite - all should pass
pbl test
```

## Step 4: Manually Validate and Clone the Base Image (if desired)

After completing step 3, the microSD card is fully configured, but not yet individualized
(unique password/hostname). This is the best time to verify that the distribution behaves
as expected and freeze it for mass cloning.

To clone a microSD card, use `dd` on Linux/macOS to write it to an `.img` file and then
compress that (e.g. with `.xz`). Alternatively, use a hardware microSD duplicator.


## Step 5: Individualize a microSD Card to a Pi

This step individualizes the image, which makes it unique for a particular group/box.

All microSD cards are essentially identical to each other - apart from their hostname and
password. The hostname is important because institutional networks tend to use it when
listing devices connected to networks (e.g. `TUD-Facility` portal does this). The password
is important because it reduces the chance of a student connecting to another group's Pi
by accident.

To individualize a Pi, run TODO on the Pi. It will prompt for a hostname and password, which
need to be manually typed in.

**Add the `hostname` and `password` to the organizational spreadsheet**.

## Step 2: Install 

These steps setup the Pi's microSD card with the necessary OS and bootup configuration (notably: the
correct WiFi credentials, hostname, SSH, username, and password).

- Use the Raspberry Pi Imager software to flash Raspbian onto the Pi's microSD card. Click the settings
  gear to change the installation configuration:

  - Assign a unique `hostname` derived from the physical ID. For example, if the physical ID is `A` then the hostname
    should probably be something like `pblhosta`.
  - **Add the `hostname` to the spreadsheet**. The hostname is useful in various networking-related
    activities (e.g. it will be listed in your hotspot).
  - Enable SSH and use password authentication
  - Use a `username` of `pbl` for SSH authentication
  - Assign a unique `password` for each Pi. The password should be a basic easy-to-write one. For example,
    from a child's password generator or similar.
  - **Add the `password` to the spreadsheet**. The password is **required** for configuring/using the
    Pi. Do not mix this one up.
  - Configure wireless LAN to use the appropriate (e.g. bootstrap) WiFi network. The SSID of the
    network is usually related to the physical ID (e.g. if the physical ID is `A` then the wifi
    SSID should probably be `pblwifia`). The WiFi password should match the `password` of each pi.
  - Set locale/region to `Netherlands`
  - Set keyboard layout to `us`

- Write the configured OS to the microSD card
- Eject the card so that it's ready to be inserted into the Raspberry Pi


# Boot up the Raspberry Pi

Once the microSD card has been flashed with the "base" Raspberry Pi OS, it must be booted up so
that further configuration steps can be performed via SSH.

- Eject the micro SD card, plug it into the pi, power up the pi
- The pi should automatically connect to your WiFi network. Your hotspot/router software should
  identify that the Pi has connected.
- Use the IP/name listed in your hotspot/router software during the SSH configuration step.
- If you can't figure out the IP address of the Pi, you might have to cross your fingers and
  hope `hostname.local` works. Some routers will use the `hostname` you set to provide a temporary
  domain name for your device on the network.


# Configure the Pi via SSH

With the "base" Raspberry Pi OS installed, and with it logged onto a (probably, hotspot) network, you
can now use SSH to configure the Raspberry Pi with PBL-specific software and configuration options (e.g.
enable VNC and i2c).

- Use `scp` to copy the `pbl` subdirectory in `X0_SoftwareSetup` onto the Pi:

  - Open a terminal (e.g. Windows Powershell, Mac Terminal, Linux GNOME terminal)
  - Copy `pbl` to the Pi with: `scp -r pbl/ username@address:`
  - **Note 1**: `username` was set when you flashed the device. It's usually `pbl`.
  - **Note 2**: `password` was set when you flashed the device. It should've been written down in the spreadsheet.
  - **Note 3**: `address` can be the IP address (via your hotspot software), `hostname` (e.g. `pbl1`), or
    `hostname.local` - depending on how you configured your network.
  - **Note 4**: the colon (`:`) at the end of `username@address:` is important

- Use `ssh` to install the `pbl` package onto the pi and then use `pbl install` to setup the pi:
  - Open a terminal (e.g. Windows Powershell, Mac Terminal, Linux GNOME terminal)
  - Connect to the Pi with: `ssh username@address`
    - **Note 1**: `username` was set when you flashed the device. It's usually `pbl`.
    - **Note 2**: `password` was set when you flashed the device. It should've been written down in the spreadsheet.
    - **Note 3**: `address` can be the IP address (via your hotspot software), `hostname` (e.g. `pbl1`), or
      `hostname.local` - depending on how you configured your network
  - Download the PBL repository onto the pi with `git clone https://github.com/PortableBalanceLab/PBL`
  - Change to the X0_SoftwareSetup directory with `cd PBL/X0_SoftwareSetup`
  - Run `sudo pip install --force-reinstall ./pbl` to install the `pbl` package to the virtual environment
  - Ensure `apt` is up to date with `sudo apt-get update`
  - Run `sudo pbl install` to setup the Pi (system-wide) and the virtual environment

- via SSH, get the Pi's MAC address (if your hotspot software doesn't provide it):

  - Use this command: `ip link show wlan0 | grep -Po 'ether \K[^ ]*'`
  - **Add the `MAC` to the spreadsheet**. The MAC address is required for registering a device
    on managed (e.g. university) networks.

> **At this point, the Pi is fully configured** 🥳
>
> You can now clone this base "PBL" image and flash it to all Pis. **However**, you should reconfigure
> the cloned images appropriately with a unique `hostname`, user `password`, and (if necessary) SSID.
> Otherwise, all Pis will appear to be exactly the same from a network/organizational PoV.


# Test the Pi

- You should be able to connect to the Pi via VNC:

  - Install VNC Viewer. The credentials for the Pi will be to use the same `address`, `username`,
    and `password` as you used for SSH
  - You may find that you need to reset the Pi after configuration for VNC to fully work

 # Alternate Install (`rpi-clone`)

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
