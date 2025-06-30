#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)

export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${BASE_DIR}/install/lib
export PYTHONPATH=\$PYTHONPATH:${BASE_DIR}/install/lib

cd ${BASE_DIR}/apps
python kalibr_calibrate_cameras --target ${BASE_DIR}/others/aprilgrid.yaml \
 	--models pinhole-radtan pinhole-radtan --topics /camera/left /camera/right \
 	--bag /home/cat/projects/data/camera_calib.bag \
 	--bag-freq 5.0