#!/usr/bin/env python3

import argparse
import csv
import serial
from pathlib import Path

base_username = "pbl"           # All devices have the same username (doesn't change)
base_hostname = "raspberrypi"   # All not-individualized devices have this hostname
base_password = "thebasecase"   # All not-individualized devices have this pw
root_password = "therootcause"  # All devices have the same root password

# Represents a persisted lookup/database of individualized Pis
class DeviceDB:

    def __init__(self, db_path):
        self.db_path = db_path
        self.devices = []
        with open(self.db_path, "rt") as f:
            for device in csv.DictReader(f):
                self.devices.append(device)

    # Returns the password associated with `hostname`, or raises a
    # `RuntimeError` if the password cannot be found.
    def lookup_password(self, hostname):
        if hostname == base_hostname:
            return base_password
        for device in self.devices:
            if device["hostname"] == hostname:
                return device["password"]
        raise RuntimeError(f"Cannot find {hostname} in device list")

    # Returns the hostname associated with `mac_address`, else `default`.
    def get_hostname_for_mac_address(self, mac_address, default=None):
        for device in self.devices:
            if device["mac"] == mac_address:
                return device["hostname"]
        return default

    # Returns the hostname associated with `mac_address`, else `default`.
    def get_password_for_mac_address(self, mac_address, default=None):
        for device in self.devices:
            if device["mac"] == mac_address:
                return device["password"]
        return default

def do_individualization_via_serial(device_db_path, serial_port):
    # Load a db
    db = DeviceDB(device_db_path)

    with serial.Serial(serial_port, 115200, timeout=None, rtscts=False) as ser:
        # Send ENTER (newline), which makes the Pi respond with its login prompt
        # (if it hasn't already).
        ser.write(b"\n")

        # Read line-by-line until a login prompt is detected
        login_data = ser.read_until(b"login: ")

        # Parse the hostname out of the login prompt
        login_line_begin = login_data.rfind(b"\n")
        if login_line_begin == -1:
            raise RuntimeError(f"Cannot parse hostname from {login_data}")

        hostname = login_data[login_line_begin+1:-len(" login: ")].decode(encoding="utf-8")
        individualize = hostname == base_hostname
        if not individualize:
            print(f"Hostname '{hostname}' is not '{base_hostname}', assuming already individualized and will just print the mac address")

        # Send the username (might be based on hostname if already individualized)
        ser.write(f"{base_username}\n".encode("utf-8"))

        # Wait for the password prompt
        ser.read_until(b"Password: ")

        # Send the password
        password = db.lookup_password(hostname)
        ser.write(f"{password}\n".encode("utf-8"))

        # Calculate shell prompt (this is checked a lot)
        shell_prompt = f"{base_username}@{hostname}:~$".encode("utf-8")

        # Wait for initial shell prompt
        ser.read_until(shell_prompt)

        # Shell logged in! Ensure this script exits it when it closes
        try:
            # Make the terminal dumb, so that applications don't emit colors
            ser.write(b"export TERM=dumb\n")
            ser.read_until(shell_prompt)

            # Disable shell echoing (line discipline), so that responses
            # don't contain inputs
            ser.write(b"stty -echo\n")
            ser.read_until(shell_prompt)

            # Fetch the mac address of the Raspberry Pi's WiFi interface
            # (needed for private networks + lookups)
            ser.write(b"cat /sys/class/net/wlan0/address\n")
            mac_address = ser.read_until(shell_prompt)[0:-len(shell_prompt)].decode("utf-8").strip()
            if not individualize:
                print(f"------------------------------------------------------")
                print(f"              Individualization SKIPPED               ")
                print(f"------------------------------------------------------")
                print(f"Stored device details (from DB):                      ")
                print(f"                                                      ")
                print(f"    hostname    = {hostname}                          ")
                print(f"    password    = {password}                          ")
                print(f"    mac_address = {mac_address}                       ")
            else:
                save_db = False

                new_hostname = db.get_hostname_for_mac_address(mac_address)
                if not new_hostname:
                    new_hostname = input(f"hostname not found for {mac_address}, enter one")
                    db.set_hostname_for_mac_address(mac_address, new_hostname)
                    save_db = True

                new_password = db.get_password_for_mac_address(mac_address)
                if not new_password:
                    new_password = input(f"password not found for {mac_address}, enter one")
                    db.set_password_for_mac_address(mac_address, new_password)
                    save_db = True

                if save_db:
                    pass  # TODO: write updated CSV

                print(f"Running individualization with the following parameters:")
                print(f"- hostname = {new_hostname} (old = {hostname})")
                print(f"- password = {new_password} (old = {password})")
                print(f"- mac_address = {mac_address}")

                # Switch to root account to perform individualization
                root_shell_prompt = f"root@{hostname}:".encode("utf-8")
                ser.write(b"su\n")
                ser.read_until(b"Password: ")
                ser.write(f"{root_password}\n".encode("utf-8"))
                ser.read_until(root_shell_prompt)
                ser.write(f"cd /opt/PBL/X0_SoftwareSetup && ./scripts/03_individualize-pi.sh \"{new_hostname}\" \"{new_password}\"\n".encode("utf-8"))
                response = ser.read_until(root_shell_prompt).decode("utf-8")
                print(response)
                assert "Individualization Complete" in response
                print("You can now restart the Pi")
        finally:
            ser.write(b"exit\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("device_csv", help="Path to CSV file containing Pi credentials")
    parser.add_argument("serial_port", help="Path to the serial port the Pi is connected to (e.g. /dev/ttyUSB0)")
    args = parser.parse_args()
    do_individualization_via_serial(args.device_csv, args.serial_port)

if __name__ == "__main__":
    main()
