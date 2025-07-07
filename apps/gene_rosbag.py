import numpy as np
import cv2
import os
from rosbags.rosbag1 import Writer
from rosbags.typesys import Stores, get_typestore
from pathlib import Path
import shutil
from tqdm import tqdm
import argparse

# 获取 ROS 类型系统
typestore = get_typestore(Stores.ROS1_NOETIC)
IMU_MSG = typestore.types['sensor_msgs/msg/Imu']
IMAGE_MSG = typestore.types['sensor_msgs/msg/Image']

# 预先获取常用类型
Time = typestore.types['builtin_interfaces/msg/Time']
Header = typestore.types['std_msgs/msg/Header']
Quaternion = typestore.types['geometry_msgs/msg/Quaternion']
Vector3 = typestore.types['geometry_msgs/msg/Vector3']


def create_imu_message(timestamp: float, acc: np.ndarray, gyro: np.ndarray, q_orientation: list):
    """创建 IMU 消息"""
    sec = int(timestamp)
    nanosec = int(round((timestamp - sec) * 1e9))
    stamp = Time(sec=sec, nanosec=nanosec)
    header = Header(seq=0, stamp=stamp, frame_id='imu')

    q = Quaternion(w=q_orientation[0], x=q_orientation[1], y=q_orientation[2], z=q_orientation[3])
    linear_acceleration = Vector3(x=acc[0], y=acc[1], z=acc[2])
    angular_velocity = Vector3(x=gyro[0], y=gyro[1], z=gyro[2])

    imu_msg = IMU_MSG(
        header=header,
        orientation=q,
        orientation_covariance=np.zeros(9, dtype=np.float64),
        angular_velocity=angular_velocity,
        angular_velocity_covariance=np.zeros(9, dtype=np.float64),
        linear_acceleration=linear_acceleration,
        linear_acceleration_covariance=np.zeros(9, dtype=np.float64)
    )
    return imu_msg


def create_image_message(timestamp: float, image_path: str):
    """创建 Image 消息"""
    img_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_data is None:
        return None

    # 时间戳
    sec = int(timestamp)
    nanosec = int(round((timestamp - sec) * 1e9))
    stamp = Time(sec=sec, nanosec=nanosec)
    header = Header(seq=0, stamp=stamp, frame_id='camera')

    height, width = img_data.shape
    encoding = 'mono8'
    step = width
    data_array = img_data.flatten() if img_data.ndim > 1 else img_data
    if not data_array.flags['C_CONTIGUOUS']:
        data_array = np.ascontiguousarray(data_array)

    return IMAGE_MSG(
        header=header,
        height=height,
        width=width,
        encoding=encoding,
        is_bigendian=0,
        step=step,
        data=data_array
    )


def write_rosbag_from_files(imu_data_file: str, left_images_dir: str, right_images_dir: str, output_bag_file: str):
    """从 IMU 数据和图像生成 ROS bag 文件"""

    bag_path = Path(output_bag_file)
    if bag_path.exists():
        os.system(f'rm -rf {bag_path}')

    with Writer(output_bag_file) as writer:
        # 添加连接
        if imu_data_file is not None and Path(imu_data_file).exists():
            imu_connection = writer.add_connection('/imu', IMU_MSG.__msgtype__, typestore=typestore)
            
            # 写入 IMU 数据
            print("写入 IMU 数据...")
            with open(imu_data_file, 'r') as f:
                next(f)  # 跳过表头
                for line in tqdm(f, desc="Processing IMU"):
                    parts = line.strip().split(',')
                    if len(parts) < 11:
                        continue
                    timestamp = float(parts[0])
                    acc = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
                    gyro = np.array([float(parts[4]), float(parts[5]), float(parts[6])])
                    quat = [float(parts[7]), float(parts[8]), float(parts[9]), float(parts[10])]
                    msg = create_imu_message(timestamp, acc, gyro, quat)
                    ts = int(timestamp * 1e9)
                    writer.write(imu_connection, ts, typestore.serialize_ros1(msg, IMU_MSG.__msgtype__))

        if Path(left_images_dir).exists() and Path(right_images_dir).exists():
            left_conn = writer.add_connection('/camera/left', IMAGE_MSG.__msgtype__, typestore=typestore)
            right_conn = writer.add_connection('/camera/right', IMAGE_MSG.__msgtype__, typestore=typestore)

            # 写入图像数据
            left_dir = Path(left_images_dir)
            right_dir = Path(right_images_dir)
            image_files = sorted([f for f in left_dir.iterdir() if f.name.endswith('.png')], key=lambda x: x.stem)[1:]

            print("写入图像数据...")
            for file in tqdm(image_files, desc="Processing Images"):
                timestamp = float(file.stem)
                ts = int(timestamp * 1e9)
                left_path = str(file)
                right_path = str(right_dir / file.name)

                if not Path(right_path).exists():
                    print(f"跳过图像：{file.name}，右图不存在")
                    continue

                left_msg = create_image_message(timestamp, left_path)
                right_msg = create_image_message(timestamp, right_path)

                if left_msg is None or right_msg is None:
                    print(f"跳过图像：{file.name}，图像读取失败")
                    continue

                writer.write(left_conn, ts, typestore.serialize_ros1(left_msg, IMAGE_MSG.__msgtype__))
                writer.write(right_conn, ts, typestore.serialize_ros1(right_msg, IMAGE_MSG.__msgtype__))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将指定目录下的 IMU 和图像数据打包成 ROS Bag 文件")
    parser.add_argument('--root_dir', required=True, help='包含 images 和 imu_data.txt 的根目录')
    
    args = parser.parse_args()
    
    root_dir = Path(args.root_dir).resolve()
    if not root_dir.exists():
        raise FileNotFoundError(f"指定的路径不存在: {root_dir}")
        
    base_name = os.path.basename(root_dir)
    imu_data_file = root_dir / 'imu_data.txt'
    left_images_dir = root_dir / 'images/left'
    right_images_dir = root_dir / 'images/right'
    output_bag_file = root_dir / f'{base_name}.bag'

    write_rosbag_from_files(str(imu_data_file), str(left_images_dir), str(right_images_dir), str(output_bag_file))