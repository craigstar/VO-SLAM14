
class Map(object):
    """docstring for Map"""
    def __init__(self):
        self.keyframes = {}
        self.map_points = {}
        
    def insertKeyFrame(self, frame):
        print('Key frame size =', len(self.keyframes))
        self.keyframes[frame.id] = frame

    def insertMapPoint(self, map_point):
        self.map_points[map_point.id] = map_point
