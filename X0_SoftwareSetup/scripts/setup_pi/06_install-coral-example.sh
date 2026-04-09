#!/usr/bin/env bash

set -xeuo pipefail

echo "----- installing coral_example to /opt/coral_example/ -----"
sudo rm -rf /opt/coral_example/
sudo cp -a coral_example/ /opt/coral_example/
echo "----- finished installing coral_example to /opt/coral_example/ -----"

