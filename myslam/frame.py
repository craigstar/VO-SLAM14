import numpy as np
import sophus as sp

class Frame(object):
    """docstring for Frame"""
    factory_id = -1

    def __init__(self, nid, time_stamp=0, Tcw=None, camera=None, color=None, depth=None):
        self.id = nid
        self.time_stamp = time_stamp
        self.Tcw = Tcw if Tcw is not None else sp.SE3()
        self.camera = camera
        self.color = color
        self.depth = depth

    @staticmethod
    def createFrame():
        Frame.factory_id += 1
        return Frame(Frame.factory_id)

    def getCamCenter(self):
        return self.Tcw.inverse().translation()

    def isInFrame(self, pt_world):
        p_cam = self.camera.world2camera(pt_world, self.Tcw)
        if p_cam[2] < 0:
            return False
        pixel = self.camera.world2camera(pt_world, self.Tcw)

        lower_left = np.array([0, 0])
        uper_right = self.color.shape
        return np.logical_and(lower_left < pixel, pixel < uper_right).all()

    def findDepth(self, kp):
        x, y = np.around(kp.pt).astype(int)
        d = self.depth[y, x]
        if d != 0:
            return d / self.camera.depth_scale
        else:
            # check the nearby points
            dx = [-1, 0, 1, 0]
            dy = [0, -1, 0, 1]

            for i in range(4):
                d = self.depth[y + dy[i], x + dx[i]]
                if d != 0: return d / self.camera.depth_scale
        return -1
