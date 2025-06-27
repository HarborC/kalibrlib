#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)
# echo "BASE_DIR: ${BASE_DIR}"
echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${BASE_DIR}/install/lib"
echo "export PYTHONPATH=\$PYTHONPATH:${BASE_DIR}/install/lib"