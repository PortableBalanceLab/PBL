#!/usr/bin/env bash

set -xeuo pipefail

echo "----- starting ICM20948.py installation -----"
sudo cp -a ICM20948/ICM20948.py /opt/ICM20948.py
echo "----- finished ICM20948.py installation -----"
ls -la /opt  # debugging

