from kalibr_common import ImuDatasetReader, ImageDatasetReader
import os
import cv2

if __name__ == "__main__":
    bagfile = "/home/gpcv/Data3/CJG/Projects/ThirdParty/kalibr/build/camera_calib.bag"
    imutopic = "/imu"

    if not os.path.exists(bagfile):
        raise FileNotFoundError(f"Bag file not found: {bagfile}")

    print("Testing BagImuDatasetReader initialization...")
    reader = ImuDatasetReader.BagImuDatasetReader(bagfile, imutopic)

    print(f"Total messages after truncation: {reader.numMessages()}")

    print("Testing message iteration...")
    count = 0
    for timestamp, omega, alpha in reader:
        print(f"[{count}] Time: {timestamp}, Angular Velocity: {omega}, Linear Acceleration: {alpha}")
        count += 1
        if count >= 10:
            break

    imagetopic = "/camera/left"

    reader = ImageDatasetReader.BagImageDatasetReader(bagfile, imagetopic)

    print(f"Total messages after truncation: {reader.numImages()}")

    print("Testing message iteration...")
    count = 0
    for timestamp, img_data in reader:
        print(f"[{count}] Time: {timestamp}")
        cv2.imwrite(f"/home/gpcv/Data3/CJG/Projects/ThirdParty/kalibr/build/test/{timestamp}.jpg", img_data)
        count += 1
        if count >= 10:
            break

    print("✅ All tests passed.")