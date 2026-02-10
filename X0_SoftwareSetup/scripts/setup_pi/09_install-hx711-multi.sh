#!/usr/bin/env bash

set -xeuo pipefail

echo "----- starting hx711-multi installation -----"
sudo rm -rf /opt/hx711-multi/
sudo cp -ar ./hx711-multi /opt/hx711-multi/

# Also, install it system-wide as a `pip` package, so that
# students can write `import hx711_multi.hx711` in their code
# regardless of where they saved it.
sudo pip3 install /opt/hx711-multi/
echo "----- finished hx711-multi installation -----"

ls -la /opt/hx711-multi  # Debugging

