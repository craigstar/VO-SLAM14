from myslam import Config, VO, Camera, Frame
from time import time
import pypangolin as pango
import sophus as sp
import pandas as pd
import numpy as np
import cv2

# 
Config.setParameterFile('config/default.yaml')
vo = VO()

# Read data
dataset_dir = Config.get('dataset_dir')
print('dataset:', dataset_dir)
names = ['rgb_time', 'rgb_file', 'depth_time', 'depth_file']
data = pd.read_csv(dataset_dir + '/associate.txt', sep=' ', header=None, names=names)
data['rgb_file'] = dataset_dir + '/' + data['rgb_file']
data['depth_file'] = dataset_dir + '/' + data['depth_file']

# Camera instance
fx = Config.get('camera.fx')
fy = Config.get('camera.fy')
cx = Config.get('camera.cx')
cy = Config.get('camera.cy')
depth_scale = Config.get('camera.depth_scale')
camera = Camera(fx, fy, cx, cy, depth_scale)

#
for idx, row in data.iterrows():
    color = cv2.imread(row['rgb_file'])
    depth = cv2.imread(row['depth_file'], -1)

    if not color.size or not depth.size:
        continue

    frame = Frame.createFrame()
    frame.camera = camera
    frame.color = color
    frame.depth = depth
    frame.time_stamp = row['rgb_time']

    start = time()
    vo.addFrame(frame)
    elapsed = time() - start
    print('VO costs time:', elapsed)

    if vo.state == VO.LOST:
        break

    Tcw = frame.Tcw.inverse()

    # I added this line to viz key points
    color = cv2.drawKeypoints(color, vo.keypoints_cur, None)
    cv2.imshow('image', color)
    cv2.waitKey(1)

    if idx > 1:
        break

