#!/bin/bash
BASE_DIR=$(cd $(dirname $0); pwd)

cd ${BASE_DIR}/apps
python generate_aprilgrid_yaml.py --output others/aprilgrid.yaml -s 0.0275

cd ${BASE_DIR}/../..

# 忽略 Ctrl+C，防止脚本中断
trap '' INT
echo "开始录制数据，按 Ctrl+C 停止录制..."
# 在子 shell 中运行，恢复 Ctrl+C 功能
(
    trap - INT  # 恢复默认的 Ctrl+C 处理
    ./build/apps/record_data 2
)
trap - INT  # 恢复

source ~/rosbags_env/bin/activate

cd ${BASE_DIR}/apps
echo "开始生成 ROS bag 文件..."
python gene_rosbag.py --root_dir ../../../calib_data/camera_imu_calib

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:${BASE_DIR}/install/lib
export PYTHONPATH=$PYTHONPATH:${BASE_DIR}/install/lib

echo "开始标定..."
python kalibr_calibrate_imu_camera --target ${BASE_DIR}/apps/others/aprilgrid.yaml \
    --imu ${BASE_DIR}/apps/others/imu.yaml --imu-models calibrated \
    --cam ../../../calib_data/camera_calib/camera_calib-camchain.yaml \
    --bag ../../../calib_data/camera_imu_calib/camera_imu_calib.bag --timeoffset-padding 0.1

cd ${BASE_DIR}/../..
python scripts/calib_generation.py --input calib_data/camera_imu_calib/camera_imu_calib-camchain-imucam.yaml --output config/ours/kalibr_imucam_chain.yaml
