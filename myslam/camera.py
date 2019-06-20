import numpy as np

class Camera(object):
    """Pinhole RGB-D Camera Model"""
    def __init__(self, fx, fy, cx, cy, depth_scale=0):
        self.fx = fx
        self.fy = fy
        self.cx = cx
        self.cy = cy
        self.depth_scale = depth_scale

    def world2camera(self, pw, Tcw):
        return Tcw * pw

    def camera2world(self, pc, Tcw):
        return Tcw.inverse() * pc

    def camera2pixel(self, pc):
        return np.array([self.fx * pc[0] / pc[2] + self.cx,
                         self.fy * pc[1] / pc[2] + self.cy])

    def pixel2camera(self, pp, depth=1):
        return np.array([(pp[0] - self.cx) * depth / self.fx,
                         (pp[1] - self.cy) * depth / self.fy,
                         depth])

    def world2pixel(self, pw, Tcw):
        return self.camera2pixel(self.world2camera(pw, Tcw))

    def pixel2world(self, pp, Tcw, depth=1):
        return self.camera2world(self.pixel2camera(pp, depth), Tcw)
