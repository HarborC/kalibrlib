from rosbags.highlevel import AnyReader
from pathlib import Path
import os
import sm
import numpy as np
import aslam_cv as acv

class BagImuDatasetReaderIterator(object):
    def __init__(self,dataset,indices=None):
        self.dataset = dataset
        if indices is None:
            self.indices = np.arange(dataset.numMessages())
        else:
            self.indices = indices
        self.iter = self.indices.__iter__()
    def __iter__(self):
        return self
    def next(self):
        # required for python 2.x compatibility
        idx = next(self.iter)
        return self.dataset.getMessage(idx)
    def __next__(self):
        idx = next(self.iter)
        return self.dataset.getMessage(idx)

class BagImuDatasetReader(object):
    def __init__(self, bagfile, imutopic, bag_from_to=None, perform_synchronization=False):
        self.bagfile = bagfile
        self.topic = imutopic
        self.perform_synchronization = perform_synchronization
        self.bag = AnyReader([Path(self.bagfile)])
        self.bag.open()
        self.uncompress = None
        if imutopic is None:
            raise RuntimeError("Please pass in a topic name referring to the imu stream in the bag file\n{0}".format(self.bag));

        # Get the message indices
        self.imu_messages = list(self.bag.messages(connections=self.bag.topics[self.topic].connections))
        
        try:
            self.index = np.arange(len(self.imu_messages))
        except:
            raise RuntimeError("Could not find topic {0} in {1}.".format(imutopic, self.bagfile))
        
        self.indices = np.arange(len(self.index))
        
        #sort the indices by header.stamp
        self.indices = self.sortByTime(self.indices)
        
        #go through the file and remove the indices outside the timespan [bag_start_time, bag_end_time]
        if bag_from_to:
            self.indices = self.truncateIndicesFromTime(self.indices, bag_from_to)
            
    #sort the ros messegaes by the header time not message time
    def sortByTime(self, indices):
        timestamps=list()
        for idx in self.indices:
            connection, timestamp, rawdata = self.imu_messages[self.index[idx]]
            timestamps.append(timestamp)
        
        sorted_tuples = sorted(zip(timestamps, indices))
        sorted_indices = [tuple_value[1] for tuple_value in sorted_tuples]
        return sorted_indices
    
    def truncateIndicesFromTime(self, indices, bag_from_to):
        #get the timestamps
        timestamps=list()
        for idx in self.indices:
            connection, timestamp, rawdata = self.imu_messages[self.index[idx]]
            timestamp = timestamp * 1e-9
            timestamps.append(timestamp)

        bagstart = min(timestamps)
        baglength = max(timestamps)-bagstart
        print("bagstart", bagstart)
        print("baglength", baglength)
        #some value checking
        if bag_from_to[0]>=bag_from_to[1]:
            raise RuntimeError("Bag start time must be bigger than end time.".format(bag_from_to[0]))
        if bag_from_to[0]<0.0:
            sm.logWarn("Bag start time of {0} s is smaller 0".format(bag_from_to[0]) )
        if bag_from_to[1]>baglength:
            sm.logWarn("Bag end time of {0} s is bigger than the total length of {1} s".format(bag_from_to[1], baglength) )

        #find the valid timestamps
        valid_indices = []
        for idx, timestamp in enumerate(timestamps):
             if timestamp>=(bagstart+bag_from_to[0]) and timestamp<=(bagstart+bag_from_to[1]):
                 valid_indices.append(idx)  
        sm.logWarn("BagImuDatasetReader: truncated {0} / {1} messages.".format(len(indices)-len(valid_indices), len(indices)))
        
        return valid_indices
    
    def __iter__(self):
        # Reset the file reading
        return self.readDataset()
    
    def readDataset(self):
        return BagImuDatasetReaderIterator(self, self.indices)

    def readDatasetShuffle(self):
        indices = self.indices
        np.random.shuffle(indices)
        return BagImuDatasetReaderIterator(self, indices)

    def numMessages(self):
        return len(self.indices)
    
    def getMessage(self,idx):
        connection, timestamp, rawdata = self.imu_messages[self.index[idx]]
        secs = int(timestamp*1e-9)
        nsecs = int(timestamp - secs*1e9)
        timestamp = acv.Time(secs, nsecs)
        if connection.msgtype == 'sensor_msgs/msg/Imu':
            data = self.bag.deserialize(rawdata, connection.msgtype)
            omega = np.array([data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z])
            alpha = np.array([data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z])
            
            return (timestamp, omega, alpha)
        else:
            raise RuntimeError("The topic {0} is not sensor_msgs/msg/Imu.".format(imutopic))
