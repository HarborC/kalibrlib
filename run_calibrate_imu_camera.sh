#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)

export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${BASE_DIR}/install/lib
export PYTHONPATH=\$PYTHONPATH:${BASE_DIR}/install/lib

cd ${BASE_DIR}/apps
python kalibr_calibrate_imu_camera --target ${BASE_DIR}/others/aprilgrid.yaml \
	--imu ${BASE_DIR}/others/imu.yaml --imu-models calibrated \
	--cam /mnt/g/projects/MDBA-SLAM/SLAM/avd/hx/camera_calib/camera_calib-camchain.yaml \
	--bag /mnt/g/projects/MDBA-SLAM/SLAM/avd/hx/imu_camera_calib/imu_camera_calib_first_half2.bag --timeoffset-padding 0.1