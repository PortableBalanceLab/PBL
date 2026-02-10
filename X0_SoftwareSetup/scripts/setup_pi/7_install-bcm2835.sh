#!/usr/bin/env bash

set -xeuo pipefail

cd bcm2835
autoreconf -f -i
./configure
make
sudo make check
sudo make install

