from map import DuckietownMap
from mapviewer import MapViewer
from maptile import MapTile


class MapEditor:
    map = None
    viewer = None
    backgroundTile = MapTile('empty', 0)

    def __init__(self, map: DuckietownMap, viewer: MapViewer):
        self.map = map
        self.viewer = viewer

    # gets selection from viewer
    def copySelection(self, destX, destY):
        # TODO
        return

    def deleteSelection(self):
        # TODO
        return

    def addBorderLines(self, linesUp: int, linesRight: int, linesDown: int, linesLeft: int):
        # TODO
        return

    # Удаляет линии по краям, если все плитки в линии - фоновые
    def trimBorders(self, trimUp: bool, trimRight: bool, trimDown: bool, trimLeft: bool):
        # TODO
        return
