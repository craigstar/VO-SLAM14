import sophus as sp
from .map import Map
from .config import Config

class VO(object):
    """docstring for VO"""
    INITIALIZING = -1
    OK = 0
    LOST = 1
    
    VOState = {
        INITIALIZING: 'Initializing',
        LOST: 'LOST',
        OK: 'OK',
    }

    def __init__(self):
        self.state = VO.INITIALIZING
        self.ref = None
        self.cur = None
        self.map = Map()
        self.num_lost = 0
        self.num_inliers = 0
        self.T_c_r_estimated = sp.SE3()
        
        self.num_of_features = Config.get('number_of_features')
        self.scale_factor = Config.get('scale_factor')
        self.level_pyramid = Config.get('level_pyramid')
        self.match_ratio = Config.get('match_ratio')
        self.max_num_lost = Config.get('max_num_lost')
        self.min_inliers = Config.get('min_inliers')
        self.key_frame_min_rot = Config.get('key_frame_min_rot')
        self.key_frame_min_trans = Config.get('key_frame_min_trans')

        self.pts_3d_ref = []
        self.keypoints_cur = []
        self.descriptors_cur = np.zeros((0, 32))
        self.descriptors_ref = np.zeros((0, 32))


        self.orb = cv2.ORB_create(nfeatures=self.num_of_features, scaleFactor=self.scale_factor, nlevels=self.level_pyramid)

    def addFrame(self, frame):
        if self.state is VO.INITIALIZING:
            self.state = VO.OK
            self.cur = self.ref = frame
            self.map.insertKeyFrame(frame)
            self.extractKeyPoints()
            self.computeDescriptors()
            self.setRef3DPoints()
        elif self.state is VO.OK:
            self.cur = frame
        elif self.state is VO.LOST:
            print('VO has lost!')
        return True

    def extractKeyPoints(self):
        self.orb.detect(self.cur.color, self.keypoints_cur)

    def computeDescriptors(self):
        self.descriptors_curr = self.orb.compute(self.cur.color, self.keypoints_cur)

    def featureMatching(self):
        pass

    def setRef3DPoints(self):
        self.pts_3d_ref.clear()
        for kp, des in zip(self.keypoints_cur, self.descriptors_cur):
            d = self.ref.findDepth(kp)
            if d > 0:
                p_cam = self.ref.camera.pixel2camera(kp.pt, d)
                self.pts_3d_ref.append(p_cam)
                self.descriptors_ref.append(des)

    def poseEstimationPnP(self):
        pass

    def checkEstimatedPose(self):
        pass

    def checkKeyFrame(self):
        d = self.T_c_r_estimated.log()
        trans = d[:3]
        rot = d[-3:]
        if (np.linalg.norm(rot) > self.key_frame_min_rot or
            np.linalg.norm(trans) > self.key_frame_min_trans):
            # I dont know why he uses trans. To my knowledge, it should be self.T_c_r_estimated.tanslation()
            return True
        return False

    def addKeyFrame(self):
        print('adding a key-frame')
        self.map.insertKeyFrame(self.cur)
