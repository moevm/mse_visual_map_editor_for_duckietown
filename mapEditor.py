# -*- coding: utf-8 -*-
from map import DuckietownMap
from mapviewer import MapViewer
from collections import deque
import copy


# Don't forget call setMap on map change
class MapEditor:
    memento = None
    map = None
    viewer = None

    def __init__(self, map: DuckietownMap, viewer: MapViewer):
        self.map = map
        self.viewer = viewer
        self.memento = deque([], maxlen=150)

    @DeprecationWarning
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
        self.extendToFit(selection, destX, destY, backgroundTile)
        for i in range(len(buffer)):
            for j in range(len(buffer[i])):
                # print('paste to ['+str(destX + j)+' ; ' + str(destY + i)+ ']')
                self.map.tiles[destY + i][destX + j] = buffer[i][j]

    def extendToFit(self, selection, destX, destY, backgroundTile):
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
        for y in range(max(0, selection[1]), min(selection[3], len(self.map.tiles))):
            for x in range(max(0, selection[0]), min(selection[2], len(self.map.tiles[0]))):
                self.map.tiles[y][x] = copy.copy(backgroundTile)
        return

    # TO TEST
    def addBorderLines(self, linesUp: int, linesRight: int, linesDown: int, linesLeft: int, backgroundTile):
        for i in range(linesUp):
            l = len(self.map.tiles[0])
            self.map.tiles.insert(0, [])
            for j in range(l):
                self.map.tiles[0].append(copy.copy(backgroundTile))
        for i in range(linesDown):
            emptyLine = []
            l = len(self.map.tiles[0])
            for j in range(l):
                emptyLine.append(copy.copy(backgroundTile))
            if len(self.map.tiles[len(self.map.tiles)-1]) == 0:
                self.map.tiles[len(self.map.tiles)-1] = emptyLine
            else:
                self.map.tiles.append(emptyLine)
        for j in range(len(self.map.tiles)):
            for i in range(linesLeft):
                self.map.tiles[j].insert(0, copy.copy(backgroundTile))
            for i in range(linesRight):
                self.map.tiles[j].append(copy.copy(backgroundTile))
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

    def save(self, map):
        # deep copy
        backup = DuckietownMap()
        backup.tiles = [[]]
        for i in range(len(map.tiles)):
            backup.tiles.append([])
            for j in range(len(map.tiles[i])):
                backup.tiles[i].append(copy.copy(map.tiles[i][j]))
        if map.items:
            for i in range(len(map.items)):
                backup.items.append(map.items[i])
        if len(self.memento) == self.memento.maxlen - 1:
            self.memento.popleft()
        self.memento.append(backup)

    def undo(self):
        if len(self.memento) == 0:
            return
        self.map.items = []
        backup = self.memento.pop()
        for i in backup.items:
            self.map.items.append(i)
        self.map.tiles.clear()
        self.map.tiles.extend(backup.tiles)
