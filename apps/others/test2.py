from rosbags.highlevel import AnyReader, AnyReaderError
from pathlib import Path
import numpy as np

bag_name = Path("/home/gpcv/Data3/CJG/Projects/ThirdParty/kalibr/build/camera_calib.bag")


reader = AnyReader([bag_name])
reader.open()
# with AnyReader([bag_name]) as reader:
print(reader.duration)
print(reader.start_time)
print(reader.end_time)
print(reader.message_count)
print(reader.topics.keys())
print(len(reader.topics['/imu'].connections))
print(reader.topics['/imu'].msgcount)
print(len(reader.topics['/camera/left'].connections))
print(reader.topics['/camera/left'].msgcount)
print(len(reader.topics['/camera/right'].connections))
print(reader.topics['/camera/right'].msgcount)
imu_messages = list(reader.messages(connections=reader.topics['/imu'].connections))
connection = imu_messages[0][0]
print(imu_messages[0][0])
print(imu_messages[0][1])
rawdata = imu_messages[0][2]
print(imu_messages[0][2])
img_messages = list(reader.messages(connections=reader.topics['/camera/left'].connections))
connection2 = img_messages[0][0]
print(img_messages[0][0])

data = reader.deserialize(rawdata, connection.msgtype)
omega = np.array([data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z])
alpha = np.array([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])
print(omega)
print(alpha)