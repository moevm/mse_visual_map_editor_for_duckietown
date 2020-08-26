# -*- coding: utf-8 -*-

class MapBaseObject:
    def __init__(self, kind, position=(.0, .0), rotation=0, height=1, optional=False, static=True):
        self.kind = kind
        self.position = {}
        self.position['x'], self.position['y'] = position
        self.rotation = rotation
        self.height = height
        self.optional = optional
        self.static = static


class SignObject(MapBaseObject):

    def __init__(self, kind, **kwargs):
        MapBaseObject.__init__(self, kind, **kwargs)


class CityObject(MapBaseObject):

    def __init__(self, kind, **kwargs):
        MapBaseObject.__init__(self, kind, **kwargs)


class WatchTowerObject(MapBaseObject):

    def __init__(self, kind, **kwargs):
        MapBaseObject.__init__(self, kind, **kwargs)
        self.hostname = kwargs["hostname"]


class GroundAprilTagObject(MapBaseObject):

    def __init__(self, kind, **kwargs):
        MapBaseObject.__init__(self, kind, **kwargs)    
