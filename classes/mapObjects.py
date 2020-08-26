# -*- coding: utf-8 -*-
from .baseClass import BaseEditorClass

class MapBaseObject(BaseEditorClass):
    def __init__(self, kind, position=(.0, .0), rotation=0, height=1, optional=False, static=True):
        BaseEditorClass.__init__(self, kind, rotation)
        self.position = {}
        self.position['x'], self.position['y'] = position
        self.height = height
        self.optional = optional
        self.static = static

    def __iter__(self):
        yield from {
            'kind': self.kind,
            'height': self.height,
            'position': self.position,
            'rotation': self.rotation,
            'optional': self.optional,
            'static' : self.static
        }.items()


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
