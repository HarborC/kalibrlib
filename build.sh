#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)
echo "BASE_DIR: ${BASE_DIR}"

cd ${BASE_DIR}

rm -rf build
rm -rf install
mkdir -p build && cd build
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="../install" .. 
ninja -j$(nproc)
sudo ninja install
