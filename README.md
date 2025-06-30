# kalibrlib
该项目可以对采集的相机数据和相机IMU数据进行内外参数标定。

# 📦 依赖安装
```
# C++ 编译与数学优化相关依赖
sudo apt-get install -y libunwind-dev
sudo apt-get install -y cmake libgoogle-glog-dev libgflags-dev libatlas-base-dev libeigen3-dev libsuitesparse-dev libceres-dev

# 计算机视觉与基础库
sudo apt-get install -y libopencv-dev libboost-all-dev 

# Python GUI 与数据处理库（用于标定界面）
sudo apt install -y python3-wxgtk4.0 python3-numpy

# Python 依赖（推荐使用 venv）
pip install -r requirements.txt

```

# 🧱 编译项目
进入项目根目录，执行构建脚本：
```
cd kalibrlib
sh build.sh
```
构建完成后，生成的标定相关可执行程序与库文件将保存在 install/ 目录下。

# 🚀 启动算法
进入项目根目录，执行构建脚本：

## ✅ 相机内参标定（单/多目）
执行以下脚本前，请根据实际数据修改 --bag 参数（即 rosbag 文件路径）：
```
cd kalibrlib
sh run_calibrate_cameras.sh
```
此脚本将自动调用标定流程，完成各相机的内参与畸变参数估计。

## 相机-IMU 外参标定（联合标定）
执行前请确保修改了以下参数：

- --cam：相机配置文件路径

- --bag：包含图像与 IMU 数据的 rosbag 路径
```
cd kalibrlib
sh run_calibrate_imu_camera.sh
```
该脚本将运行相机与 IMU 的时间对齐与外参估计过程