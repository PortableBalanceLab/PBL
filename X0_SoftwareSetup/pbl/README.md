# `pbl`: Support Code for the PortableBalanceLab Course

> ℹ️ **Note**: If you're a student on the course, then you probably don't need to install
> or use this code. It's provided here in case you're interested, or need to reinstall
> something.

> 📕**tl;dr**: If you need to (re)install the `pbl` python code on a Raspberry Pi, then run
> these commands in a terminal:
>
> ```bash
> cd $(mktemp -d)
> git clone https://github.com/PortableBalanceLab/PBL
> sudo pip install --force-reinstall ./PBL/X0_SoftwareSetup/pbl
> ```

This is a tiny python package that contains support code for the PortableBalanceLab
course. It is designed to be installed on a fresh Raspberry Pi and then used to flash
and check the Pi

# Installation

This is a standard `setuptools`-based python package. You can install it locally by
copying it to the Raspberry Pi and then running something like:

```bash
pip install ./pbl

# or, if you want to ensure you're installing the version you copied system-wide:
sudo pip install --force-reinstall ./pbl
```
