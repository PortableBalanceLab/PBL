#!/usr/bin/env bash

set -xeuo pipefail

echo "----- copying project-posenet to /opt/project-posenet/ -----"
sudo rm -rf /opt/project-posenet
sudo cp -ra ./project-posenet/ /opt/project-posenet
echo "----- finished copying project-posenet to /opt/project-posenet/"

# Print project-posenet directory (debugging)
ls -la /opt/project-posenet
