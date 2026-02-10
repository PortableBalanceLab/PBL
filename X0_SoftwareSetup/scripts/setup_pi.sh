#!/usr/bin/env bash

set -xeuo pipefail

echo "----- starting install of PBL dependencies -----"
for install_script in ./scripts/setup_pi/*; do
    echo "----- running ${install_script} -----"
    ${install_script};
done
echo "----- finished install of PBL dependencies: enjoy :> -----"

