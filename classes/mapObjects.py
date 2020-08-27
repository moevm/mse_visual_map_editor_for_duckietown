# -*- coding: utf-8 -*-
from .baseClass import BaseEditorClass


class MapBaseObject(BaseEditorClass):
    def __init__(self, init_info):
        BaseEditorClass.__init__(self, init_info)
        self.position = {}
        self.position['x'], self.position['y'] = init_info['pos']
        self.height = init_info['height']
        self.optional = init_info['optional']
        self.static = init_info['static']

    def __iter__(self):
        yield from {
            'kind': self.kind,
            'height': self.height,
            'position': self.position,
            'rotation': self.rotation,
            'optional': self.optional,
            'static': self.static
        }.items()


class SignObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)


class CityObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)


class WatchTowerObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)
        self.hostname = init_info["hostname"]


class GroundAprilTagObject(MapBaseObject):

    def __init__(self, init_info):
        MapBaseObject.__init__(self, init_info)
