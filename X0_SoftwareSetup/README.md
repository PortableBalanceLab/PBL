# `X0`: Extra Content 0: Software Setup

> ℹ️ **Note**: If you're a student on the course, then you probably don't need to **do** anything
> on this page. The organizers have already done this for you. This is provided for your information.

This guide sets up a Raspberry Pi (Zero or 4) from scratch such that it's ready for use in the
practical labs (content beginning with `S`).

You will use the Raspberry Pi Imager software for this. Download it from: https://www.raspberrypi.com/software/


# Create a Spreadsheet for Tracking Pi Credentials/Information

Use whatever you prefer (e.g. google doc). The spreadsheet will have the following columns:

- `ID`: unique physical ID that was written on the Pi
- `SSID`: WiFi SSID that the Pi will automatically join on power-on
- `WiFi Password`: pssword for the WiFi network identified by `SSID`
- `hostname`: unique virtual hostname for this Pi
- `password`: password for the `pbl` account
- `MAC`: physical MAC address of the Pi

This information is filled out while setting up the Pi.


# Physically ID the Pi

- Use a permanant marker to physically write an ID on the Pi somewhere (e.g. it can just be a number).
- Write the same ID on the SD card
- **Add the `ID` to the spreadsheet**. The ID is useful to have in case Pis are mixed up, or for cross-checking with
  other information.


# Setup WiFi

In order to avoid having to physically wire up each Raspberry Pi to power, a monitor, a keyboard, and
a mouse, this guide instead opts for configuring the Raspberry Pi such that it already uses a known
WiFi SSID and password combination on first boot. With that, the Pi will immediately join a network, and
it can then be configured entirely via SSH.

> This guide assumes you don't have an easy-to-login-to WiFi network (e.g. your home network). Instead,
> it assumes that you are on a private network with annoying WiFi credential requirements (e.g. a university
> campus).
>
> - **Easy case (e.g. home network)**: You might just be able to flash the Pi with your home network
>   credentials and entirely skip the rest of this section. You can configure the Pi via SSH through
>   your home network (e.g. using the address `hostname.local`)
>
> - **Hard case (e.g. university network)**: You will first create an easy-to-login-to local WiFi
>   hotspot from your laptop as a **bootstrap** network that the Pi will join. You then use the
>   bootstrap network to configure the Pi via SSH (incl. configuring a "proper" network).
>
> This section outlines the **hard case**, because it is assumed that you're configuring the Pis
> on a campus/company network.

- Create a "bootstrap" WiFi network from your configuring laptop (e.g. on Windows, there's the
  "mobile hotspot" feature for doing this)

  - Set the SSID of your bootstrap network to something memorable (e.g. `PBLBootstrap`). **Note**: you
    may want to change the SSID every 5-10 Pis.
  - Set the WiFi password to something memorable (e.g. `bootstrap123`)
  - Make sure your hotspot is using a 2.4 GHz band (compatibility)
  - **Add the `SSID` and `WiFi Password` to the spreadsheet**. The WiFi credentials are necessary to have
    if (e.g.) recycling the hotspot in later configuration stages.


# Flash the Pi's MicroSD Card

These steps setup the Pi's microSD card with the necessary OS and bootup configuration (notably: the
correct WiFi credentials, hostname, SSH, username, and password).

- Use the Raspberry Pi Imager software to flash Raspbian onto the Pi's microSD card. Click the settings
  gear to change the installation configuration:

  - Assign a unique `hostname` (e.g. `pbl1`). It's usually a good idea for `hostname` to be related to
    the physical ID of the Pi (e.g. if you write `1` on the Pi then assign the hostname as `pbl1` or
    similar).
  - **Add the `hostname` to the spreadsheet**. The hostname is useful in various networking-related
    activities (e.g. it will be listed in your hotspot).
  - Enable SSH and use password authentication
  - Use a `username` of `pbl`
  - Assign a unique `password` for each Pi. The password should be a basic easy-to-write one.
  - **Add the `password` to the spreadsheet**. The password is **required** for configuring/using the
    Pi. Do not mix this one up.
  - Configure wireless LAN to use the appropriate (e.g. bootstrap) network 
  - Set locale/region to `Netherlands`
  - Set keyboard layout to `us`

- Write the configured OS to the microSD card
- Eject the micro SD card, plug it into the pi, power up the pi
- The pi should automatically connect to your WiFi network. Your hotspot/router software should
  identify that the Pi has connected.
- Use the IP/name listed in your hotspot/router software during the SSH configuration step.
- If you can't figure out the IP address of the Pi, you might have to cross your fingers and
  hope `hostname.local` works. Some routers will use the `hostname` you set to provide a temporary
  domain name for your device on the network.


# Configure the Pi via SSH

With the Pi OS setup and logged into a network, you can now remotely configure the userspace side
of the Pi using SSH.

- Connect to the Pi via SSH:

  - Use a terminal (e.g. Windows Powershell, Mac Terminal) to connect
  - Command: `ssh username@address`
  - `address` can be the IP address, `hostname`, or `hostname.local`, depending on how the network
    is configured

- Copy `InstallPBLSoftware.sh` onto the Pi:

  - `InstallPBLSoftware.sh` is available in this README's directory
  - You can copy things to the Pi by running this command on your laptop (**not** in the SSH session): `scp InstallPBLSoftware.sh username@address:`
  - You can also use something like a private gist, or pre-copy the script onto the microSD and
    use it from `/boot`, etc.

- via SSH, get the Pi's MAC address:

  - Use this command: `ip link show wlan0 | grep -Po 'ether \K[^ ]*'`
  - **Add the `MAC` to the spreadsheet**. The MAC address is required for registering a device
    on managed (e.g. university) networks.
  - (you might get lucky and see it via your hotspot UI also)

- via SSH, run the `InstallPBLSoftware.sh` script:

  - The script fully configures the Pi with VNC, i2c, camera, SPI, and all of the software
    used throughout the PBL course

  - Read the script for further information

- The Pi is now fully configured 🥳


# Test the Pi

- You should be able to connect to the Pi via VNC:

  - Install VNC Viewer. The credentials for the Pi will be to use the same `address`, `username`,
    and `password` as you used for SSH
  - You may find that you need to reset the Pi after configuration for VNC to fully work
