#!/bin/bash
BASE_DIR=$(cd $(dirname $0);pwd)

cd ${BASE_DIR}/../..

# 忽略 Ctrl+C，防止脚本中断
trap '' INT
echo "开始录制数据，按 Ctrl+C 停止录制..."
# 在子 shell 中运行，恢复 Ctrl+C 功能
(
    trap - INT  # 恢复默认的 Ctrl+C 处理
    ./build/apps/record_data 1
)
trap - INT  # 恢复

source ~/rosbags_env/bin/activate

cd ${BASE_DIR}/apps
python gene_rosbag.py --root_dir ../../../calib_data/camera_calib

export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:${BASE_DIR}/install/lib
export PYTHONPATH=\$PYTHONPATH:${BASE_DIR}/install/lib

python kalibr_calibrate_cameras --target ${BASE_DIR}/apps/others/aprilgrid.yaml \
 	--models pinhole-radtan pinhole-radtan --topics /camera/left /camera/right \
 	--bag ../../../calib_data/camera_calib/camera_calib.bag \
 	--bag-freq 5.0