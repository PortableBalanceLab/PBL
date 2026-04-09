#!/usr/bin/env bash

set -xeuo pipefail

KEYRING_DIR="/usr/share/keyrings"
KEYRING_FILE="${KEYRING_DIR}/google-coral-edgetpu.gpg"

echo "----- configuring apt installation steps -----"

# Create keyrings directory if it doesn't exist
sudo mkdir -p -m 755 "$KEYRING_DIR"

# Download the key, dearmor it (convert to binary), and save it to the keyring dir.
# We use 'gpg --dearmor' because 'apt' prefers binary keyrings over ASCII (.gpg vs .asc)
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
    gpg --dearmor | \
    sudo tee "$KEYRING_FILE" > /dev/null

# Add the google repo: ensure it always uses the gpg key when checking the signatures
echo "deb [signed-by=$KEYRING_FILE] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | \
    sudo tee /etc/apt/sources.list.d/coral-edgetpu.list

echo "----- finished configuring apt -----"

# Ensure all apt lists are up-to-date
echo "----- updating apt -----"
sudo apt update
echo "----- finished updating apt -----"
