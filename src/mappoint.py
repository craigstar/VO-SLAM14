import numpy as np


class MapPoint(object):
    """docstring for MapPoint"""
    factory_id = 0

    def __init__(self, nid, position, norm):
        self.id = nid
        self.pos = position
        self.norm = norm
        self.observed_times = 0
        self.correct_times = 0

    @staticmethod
    def createMapPoint():
        MapPoint.factory_id += 1
        return MapPoint(MapPoint.factory_id, np.zeros(3), np.zeros(3))
