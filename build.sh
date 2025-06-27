#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)
echo "BASE_DIR: ${BASE_DIR}"

cd ${BASE_DIR}

mkdir -p build && cd build
clear
cmake -G "Ninja" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="../install" .. 
ninja -j2
sudo ninja install
