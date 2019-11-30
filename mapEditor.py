from map import DuckietownMap
from mapviewer import MapViewer
from maptile import MapTile
import copy

# Don't forget call setMap on map change
class MapEditor:
    map = None
    viewer = None
    backgroundTile = MapTile('empty', 0)

    def __init__(self, map: DuckietownMap, viewer: MapViewer):
        self.map = map
        self.viewer = viewer

    def setMap(self, newMap: DuckietownMap):
        self.map = newMap

    def __createBuffer(self):
        buffer = [[]] * (self.viewer.tileSelection[3] - self.viewer.tileSelection[1])
        for i in range(len(buffer)):
            for j in range(self.viewer.tileSelection[2] - self.viewer.tileSelection[0]):
                buffer[i][j] = copy.copy(
                    self.map.tiles[self.viewer.tileSelection[1] + i][self.viewer.tileSelection[1] + j])
        return buffer

    def __extendAndPasteBuffer(self, buffer, destX, destY):
        u, r, d, l = 0, 0, 0, 0
        if destX < 0:
            l = -destX
            destX = 0
        elif destX + (self.viewer.tileSelection[2] - self.viewer.tileSelection[0]) > len(self.map.tiles[0]):
            r = destX + (self.viewer.tileSelection[2] - self.viewer.tileSelection[0]) - len(self.map.tiles[0])
        if destY < 0:
            u = -destY
            destY = 0
        elif destY + (self.viewer.tileSelection[3] - self.viewer.tileSelection[1]) > len(self.map.tiles):
            d = destY + (self.viewer.tileSelection[3] - self.viewer.tileSelection[1]) - len(self.map.tiles)
        self.addBorderLines(u, r, d, l)
        for i in range(len(buffer)):
            for j in range(len(buffer[0])):
                self.map.tiles[destY + i][destX + j] = buffer[i][j]

    # TO TEST
    def copySelection(self, destX, destY):
        buffer = self.__createBuffer()
        self.__extendAndPasteBuffer(buffer, destX, destY)
        return

    # TO TEST
    def moveSelection(self, destX, destY):
        buffer = self.__createBuffer()
        self.deleteSelection()
        self.__extendAndPasteBuffer(buffer, destX, destY)
        return

    # TO TEST
    def deleteSelection(self):
        selection = self.viewer.tileSelection
        for y in range(max(0, selection[1]), max(0, selection[3])):
            for x in range(max(0, selection[0]), max(0, selection[2])):
                self.map.tiles[y][x] = copy.copy(self.backgroundTile)
        return

    # TO TEST
    def addBorderLines(self, linesUp: int, linesRight: int, linesDown: int, linesLeft: int):
        emptyLine = [copy.copy(self.backgroundTile)] * (len(self.map.tiles[0]) if len(self.map.tiles) > 0 else 0)
        for i in range(linesUp):
            self.map.tiles.insert(0, emptyLine)
        for i in range(linesDown):
            self.map.tiles.append(emptyLine)
        for j in range(len(self.map.tiles)):
            for i in range(linesLeft):
                self.map.tiles[j].insert(0, copy.copy(self.backgroundTile))
            for i in range(linesRight):
                self.map.tiles[j].append(copy.copy(self.backgroundTile))
        return

    # Удаляет линии по краям, если все плитки в линии - фоновые
    # TO TEST
    def trimBorders(self, trimUp: bool, trimRight: bool, trimDown: bool, trimLeft: bool):
        isLineEmpty = True
        if trimDown:
            while isLineEmpty:
                for i in range(len(self.map.tiles[0])):
                    if self.map.tiles[len(self.map.tiles)-1][i] != self.backgroundTile:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    self.map.tiles.pop()
        isLineEmpty = True
        if trimUp:
            while isLineEmpty:
                for i in range(len(self.map.tiles[0])):
                    if self.map.tiles[0][i] != self.backgroundTile:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    self.map.tiles.pop(0)
        isLineEmpty = True
        if trimRight:
            while isLineEmpty:
                for i in range(len(self.map.tiles)):
                    if self.map.tiles[i][len(self.map.tiles[i])-1] != self.backgroundTile:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    for i in range(len(self.map.tiles)):
                        self.map.tiles[i].pop()
        isLineEmpty = True
        if trimLeft:
            while isLineEmpty:
                for i in range(len(self.map.tiles)):
                    if self.map.tiles[i][0] != self.backgroundTile:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    for i in range(len(self.map.tiles)):
                        self.map.tiles[i].pop(0)
        return
