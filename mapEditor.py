from map import DuckietownMap
from mapviewer import MapViewer
from maptile import MapTile
import copy


# Don't forget call setMap on map change
class MapEditor:
    map = None
    viewer = None


    def __init__(self, map: DuckietownMap, viewer: MapViewer):
        self.map = map
        self.viewer = viewer

    def setMap(self, newMap: DuckietownMap):
        self.map = newMap

    def __createBuffer(self, selection):
        buffer = []
        for i in range(selection[3] - selection[1]):
            buffer.append([])
            for j in range(selection[2] - selection[0]):
                buffer[i].append(copy.copy(
                    self.map.tiles[selection[1] + i][selection[0] + j]))
                # buffer[i][j] = copy.copy(
                #     self.map.tiles[selection[1] + i][selection[0] + j])
        return buffer

    def __extendAndPasteBuffer(self, selection, buffer, destX, destY, backgroundTile):
        self.extendToFit(selection,destX,destY,backgroundTile)
        for i in range(len(buffer)):
            for j in range(len(buffer[i])):
                # print('paste to ['+str(destX + j)+' ; ' + str(destY + i)+ ']')
                self.map.tiles[destY + i][destX + j] = buffer[i][j]

    def extendToFit(self, selection, destX, destY,backgroundTile):
        u, r, d, l = 0, 0, 0, 0
        if destX < 0:
            l = -destX
            destX = 0
        elif destX + (selection[2] - selection[0]) > len(self.map.tiles[0]):
            r = destX + (selection[2] - selection[0]) - len(self.map.tiles[0])
        if destY < 0:
            u = -destY
            destY = 0
        elif destY + (selection[3] - selection[1]) > len(self.map.tiles):
            d = destY + (selection[3] - selection[1]) - len(self.map.tiles)
        self.addBorderLines(u, r, d, l, backgroundTile)

    # TO TEST
    def copySelection(self, selection, destX, destY, backgroundTile):
        buffer = self.__createBuffer(selection)
        self.__extendAndPasteBuffer(selection, buffer, destX, destY, backgroundTile)
        return

    # TO TEST
    def moveSelection(self, selection, destX, destY, backgroundTile):
        buffer = self.__createBuffer(selection)
        self.deleteSelection(selection, backgroundTile)
        self.__extendAndPasteBuffer(selection, buffer, destX, destY, backgroundTile)
        return

    # TO TEST
    def deleteSelection(self, selection, backgroundTile):
        for y in range(max(0, selection[1]), max(0, selection[3])):
            for x in range(max(0, selection[0]), max(0, selection[2])):
                self.map.tiles[y][x] = copy.copy(backgroundTile)
        return

    # TO TEST
    def addBorderLines(self, linesUp: int, linesRight: int, linesDown: int, linesLeft: int, backgroundTile):
        emptyLine = []
        for i in range(len(self.map.tiles[0])):
            emptyLine.append(backgroundTile)
        for i in range(linesUp):
            self.map.tiles.insert(0, copy.copy(emptyLine))
        for i in range(linesDown):
            self.map.tiles.append(copy.copy(emptyLine))

        for j in range(len(self.map.tiles)):
            for i in range(linesLeft):
                self.map.tiles[j].insert(0, backgroundTile)
            for i in range(linesRight):
                self.map.tiles[j].append(backgroundTile)
        return

        # Удаляет линии по краям, если все плитки в линии - фоновые
        # TO TEST

    def trimBorders(self, trimUp: bool, trimRight: bool, trimDown: bool, trimLeft: bool, backgroundTile):
        isLineEmpty = True
        if trimDown:
            while isLineEmpty:
                for i in range(len(self.map.tiles[len(self.map.tiles) - 1])):
                    if self.map.tiles[len(self.map.tiles) - 1][i].kind != backgroundTile.kind:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    self.map.tiles.pop()
        isLineEmpty = True
        if trimUp:
            while isLineEmpty:
                for i in range(len(self.map.tiles[0])):
                    if self.map.tiles[0][i].kind != backgroundTile.kind:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    self.map.tiles.pop(0)
        isLineEmpty = True
        if trimRight:
            while isLineEmpty:
                for i in range(len(self.map.tiles)):
                    if self.map.tiles[i][len(self.map.tiles[i]) - 1].kind != backgroundTile.kind:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    for i in range(len(self.map.tiles)):
                        self.map.tiles[i].pop()
        isLineEmpty = True
        if trimLeft:
            while isLineEmpty:
                for i in range(len(self.map.tiles)):
                    if self.map.tiles[i][0].kind != backgroundTile.kind:
                        isLineEmpty = False
                        break
                if isLineEmpty:
                    for i in range(len(self.map.tiles)):
                        self.map.tiles[i].pop(0)
        return


    def save(self):
        return

    def undo(self):
        return