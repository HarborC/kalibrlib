```
sudo apt-get install -y libunwind-dev
sudo apt-get install -y cmake libgoogle-glog-dev libgflags-dev libatlas-base-dev libeigen3-dev libsuitesparse-dev libceres-dev
sudo apt-get install -y libopencv-dev libboost-all-dev libpcl-dev
sudo apt install python3-wxgtk4.0 python3-numpy
```

```
python kalibr_calibrate_cameras --target ../files/aprilgrid.yaml \
 	--models pinhole-radtan pinhole-radtan --topics /camera/left /camera/right \
 	--bag /home/cat/projects/data/camera_calib.bag \
 	--bag-freq 5.0
```

```
python kalibr_calibrate_imu_camera --target ../files/aprilgrid.yaml \
	--imu /mnt/g/projects/MDBA-SLAM/SLAM/avd/hx/imu_calib/imu.yaml --imu-models calibrated \
	--cam /mnt/g/projects/MDBA-SLAM/SLAM/avd/hx/camera_calib/camera_calib-camchain.yaml \
	--bag /mnt/g/projects/MDBA-SLAM/SLAM/avd/hx/imu_camera_calib/imu_camera_calib_first_half2.bag --timeoffset-padding 0.1
```