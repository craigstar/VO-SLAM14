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
        
        self.num_of_features = Config.get('number_of_features')
        self.scale_factor = Config.get('scale_factor')
        self.level_pyramid = Config.get('level_pyramid')
        self.match_ratio = Config.get('match_ratio')

