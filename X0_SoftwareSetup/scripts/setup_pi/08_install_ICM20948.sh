#!/usr/bin/env bash

set -xeuo pipefail

echo "----- starting ICM20948.py + IMU_test.py installation -----"
sudo cp -a ICM20948/ICM20948.py ICM20948/IMU_test.py /opt/
echo "----- finished ICM20948.py + IMU_test.py installation -----"

ls -la /opt  # debugging
