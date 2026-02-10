#!/usr/bin/env bash

set -xeuo pipefail

tmp_dir=$(mktemp -d)
cp -a bcm2835/ ${tmp_dir}
cd ${tmp_dir}/bcm2835/
autoreconf -f -i
./configure
make
sudo make check
sudo make install
cd -
rm -rf ${tmp_dir}
