from rosbags.highlevel import AnyReader
from pathlib import Path
import cv2
import os
import numpy as np
import aslam_cv as acv
import sm

class BagImageDatasetReaderIterator(object):
  def __init__(self, dataset, indices=None):
    self.dataset = dataset
    if indices is None:
      self.indices = np.arange(dataset.numImages())
    else:
      self.indices = indices
    self.iter = self.indices.__iter__()

  def __iter__(self):
    return self

  def next(self):
    # required for python 2.x compatibility
    idx = next(self.iter)
    return self.dataset.getImage(idx)

  def __next__(self):
    idx = next(self.iter)
    return self.dataset.getImage(idx)


class BagImageDatasetReader(object):
  def __init__(self, bagfile, imagetopic, bag_from_to=None, perform_synchronization=False, bag_freq=None):
    self.bagfile = bagfile
    self.topic = imagetopic
    self.perform_synchronization = perform_synchronization
    self.bag = AnyReader([Path(self.bagfile)])
    self.bag.open()
    self.uncompress = None
    if imagetopic is None:
      raise RuntimeError(
          "Please pass in a topic name referring to the image stream in the bag file\n{0}".format(self.bag))

    self.image_messages = list(self.bag.messages(connections=self.bag.topics[self.topic].connections))

    try:
      self.index = np.arange(len(self.image_messages))
    except:
      raise RuntimeError("Could not find topic {0} in {1}.".format(imagetopic, self.bagfile))

    self.indices = np.arange(len(self.index))

    # sort the indices by header.stamp
    self.indices = self.sortByTime(self.indices)

    # go through the bag and remove the indices outside the timespan [bag_start_time, bag_end_time]
    if bag_from_to:
      self.indices = self.truncateIndicesFromTime(self.indices, bag_from_to)

    # go through and remove indices not at the correct frequency
    if bag_freq:
      self.indices = self.truncateIndicesFromFreq(self.indices, bag_freq)

  # sort the ros messegaes by the header time not message time
  def sortByTime(self, indices):
    self.timestamp_corrector = sm.DoubleTimestampCorrector()
    timestamps = list()
    for idx in self.indices:
      connection, timestamp, rawdata = self.image_messages[self.index[idx]]
      timestamps.append(timestamp)

    sorted_tuples = sorted(zip(timestamps, indices))
    sorted_indices = [tuple_value[1] for tuple_value in sorted_tuples]
    return sorted_indices

  def truncateIndicesFromTime(self, indices, bag_from_to):
    # get the timestamps
    timestamps = list()
    for idx in self.indices:
      connection, timestamp, rawdata = self.image_messages[self.index[idx]]
      timestamp = timestamp * 1e-9
      timestamps.append(timestamp)

    bagstart = min(timestamps)
    baglength = max(timestamps) - bagstart

    # some value checking
    if bag_from_to[0] >= bag_from_to[1]:
      raise RuntimeError("Bag start time must be bigger than end time.".format(bag_from_to[0]))
    if bag_from_to[0] < 0.0:
      sm.logWarn("Bag start time of {0} s is smaller 0".format(bag_from_to[0]))
    if bag_from_to[1] > baglength:
      sm.logWarn("Bag end time of {0} s is bigger than the total length of {1} s".format(bag_from_to[1], baglength))

    # find the valid timestamps
    valid_indices = []
    for idx, timestamp in enumerate(timestamps):
      if timestamp >= (bagstart + bag_from_to[0]) and timestamp <= (bagstart + bag_from_to[1]):
        valid_indices.append(idx)
    sm.logWarn(
        "BagImageDatasetReader: truncated {0} / {1} images (from-to).".format(len(indices) - len(valid_indices), len(indices)))
    return valid_indices

  def truncateIndicesFromFreq(self, indices, freq):

    # some value checking
    if freq < 0.0:
      raise RuntimeError("Frequency {0} Hz is smaller 0".format(freq))

    # find the valid timestamps
    timestamp_last = -1
    valid_indices = []
    for idx in self.indices:
      connection, timestamp, rawdata = self.image_messages[self.index[idx]]
      timestamp = timestamp * 1e-9
      if timestamp_last < 0.0:
        timestamp_last = timestamp
        valid_indices.append(idx)
        continue
      if (timestamp - timestamp_last) >= 1.0 / freq:
        timestamp_last = timestamp
        valid_indices.append(idx)
    sm.logWarn("BagImageDatasetReader: truncated {0} / {1} images (frequency)".format(len(indices) - len(valid_indices), len(indices)))
    return valid_indices

  def __iter__(self):
    # Reset the bag reading
    return self.readDataset()

  def readDataset(self):
    return BagImageDatasetReaderIterator(self, self.indices)

  def readDatasetShuffle(self):
    indices = self.indices
    np.random.shuffle(indices)
    return BagImageDatasetReaderIterator(self, indices)

  def numImages(self):
    return len(self.indices)

  def imgmsg_to_cv2(self, img_msg):
    height = img_msg.height
    width = img_msg.width
    encoding = img_msg.encoding
    data = img_msg.data

    if encoding == "8UC1" or encoding == "mono8":
        dtype = np.uint8
        channels = 1
    elif encoding == "8UC3" or encoding == "bgr8" or encoding == "rgb8":
        dtype = np.uint8
        channels = 3
    elif encoding == "8UC4" or encoding == "bgra8":
        dtype = np.uint8
        channels = 4
    elif encoding == "16UC1" or encoding == "mono16":
        dtype = np.uint16
        channels = 1
    elif encoding.startswith("bayer_"):
        dtype = np.uint8
        channels = 1
    else:
        raise ValueError(f"Unsupported encoding: {encoding}")

    image_np = np.frombuffer(data, dtype=dtype)
    img_shape = (height, width) if channels == 1 else (height, width, channels)
    return image_np.reshape(img_shape)

  def getImage(self, idx):
    connection, timestamp, rawdata = self.image_messages[self.index[idx]]
    # print(timestamp)
    secs = int(timestamp*1e-9)
    nsecs = int(timestamp - secs*1e9)
    timestamp = acv.Time(secs, nsecs)

    if connection.msgtype == 'sensor_msgs/msg/CompressedImage':
      compressed_msg = self.bag.deserialize(rawdata, connection.msgtype)
      np_arr = np.frombuffer(compressed_msg.data, dtype=np.uint8)
      img_data = cv2.imdecode(np_arr, cv2.IMREAD_UNCHANGED)
      if len(img_data.shape) > 2 and img_data.shape[2] == 3:
        img_data = cv2.cvtColor(img_data, cv2.COLOR_BGR2GRAY)
    elif connection.msgtype == 'sensor_msgs/msg/Image':
      msg = self.bag.deserialize(rawdata, connection.msgtype)
      cv_image = self.imgmsg_to_cv2(msg)
      if msg.encoding in ["16UC1", "mono16"]:
        img_data = (cv_image / 256).astype(np.uint8)
      elif msg.encoding in ["8UC1", "mono8"]:
        img_data = cv_image
      elif msg.encoding in ["8UC3", "bgr8"]:
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
      elif msg.encoding == "rgb8":
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)
      elif msg.encoding in ["8UC4", "bgra8"]:
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2GRAY)
      elif msg.encoding == "bayer_rggb8":
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BAYER_BG2GRAY)
      elif msg.encoding == "bayer_bggr8":
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BAYER_RG2GRAY)
      elif msg.encoding == "bayer_gbrg8":
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BAYER_GR2GRAY)
      elif msg.encoding == "bayer_grbg8":
        img_data = cv2.cvtColor(cv_image, cv2.COLOR_BAYER_GB2GRAY)
      else:
        raise RuntimeError(
            "Unsupported Image Encoding: '{}'\nSupported are: "
            "16UC1 / mono16, 8UC1 / mono8, 8UC3 / rgb8 / bgr8, 8UC4 / bgra8, "
            "bayer_rggb8, bayer_bggr8, bayer_gbrg8, bayer_grbg8".format(data.encoding))
    else:
      raise RuntimeError(
        "Unsupported Image Type: '{}'\nSupported are: "
        "mv_cameras/ImageSnappyMsg, sensor_msgs/CompressedImage, sensor_msgs/Image".format(data._type))
    return (timestamp, img_data)
