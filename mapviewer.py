# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtCore, QtGui, QtWidgets
from map import DuckietownMap
from utils import get_list_dir_with_path

TILES_DIR_PATH = './img/tiles'
OBJECT_DIR_PATHS = ['./img/signs',
                    './img/apriltags',
                    './img/objects']


class MapViewer(QGraphicsView, QtWidgets.QWidget):
    map = None
    tileSprites = {'empty': QtGui.QImage()}
    objects = {'stop': QtGui.QImage()}
    offsetX = 0
    offsetY = 0
    sc = 1
    rmbPressed = False
    lmbPressed = False
    rmbPrevPos = [0, 0]
    mouseStartX, mouseStartY = 0, 0
    mouseCurX, mouseCurY = 0, 0
    #  Stores the top left and bottom right coordinates of the selected area (including zero size areas) as array indexes
    #  If the selection is outside the array to the left, contains -1
    #  If the selection is outside the array to the right - width / height
    tileSelection = [0] * 4
    selectionChanged = QtCore.pyqtSignal()
    lmbClicked = QtCore.pyqtSignal(int, int)  #  click coordinates as an index of the clicked tile

    def __init__(self):
        QGraphicsView.__init__(self)
        self.setScene(QtWidgets.QGraphicsScene())
        # load tiles
        for filename, file_path in get_list_dir_with_path(TILES_DIR_PATH):
            tile_name = filename.split('.')[0]
            self.tileSprites[tile_name] = QtGui.QImage()
            self.tileSprites[tile_name].load(file_path)
        # load objects
        for dir_path in OBJECT_DIR_PATHS:
            for filename, file_path in get_list_dir_with_path(dir_path):
                object_name = filename.split('.')[0]
                self.objects[object_name] = QtGui.QImage()
                self.objects[object_name].load(file_path)

    def setMap(self, tiles: DuckietownMap):
        self.map = tiles
        self.raw_selection = [0] * 4
        self.tileSelection = [0] * 4
        self.scene().update()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        sf = 2 ** (event.angleDelta().y() / 240)
        if (self.sc < 0.05 and sf < 1) or (self.sc > 100 and sf > 1):
            return
        self.sc *= sf
        self.scene().update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.lmbPressed = False
            if int((self.mouseStartX - self.offsetX) / self.sc * self.map.gridSize) == int(
                    (self.mouseCurX - self.offsetX) / self.sc * self.map.gridSize) and int(
                (self.mouseStartY - self.offsetY) / self.sc * self.map.gridSize) == int(
                (self.mouseCurY - self.offsetY) / self.sc * self.map.gridSize):
                self.lmbClicked.emit(int((self.mouseStartX - self.offsetX) / self.sc * self.map.gridSize),
                                     int((self.mouseStartY - self.offsetY) / self.sc * self.map.gridSize))
            
            self.raw_selection = [
                ((min(self.mouseStartX, self.mouseCurX) - self.offsetX) / self.sc
                                         ) / self.map.gridSize,
                ((min(self.mouseStartY, self.mouseCurY) - self.offsetY) / self.sc
                                         ) / self.map.gridSize,
                ((max(self.mouseStartX, self.mouseCurX) - self.offsetX) / self.sc) / self.map.gridSize,
                ((max(self.mouseStartY, self.mouseCurY) - self.offsetY) / self.sc) / self.map.gridSize
            ]
            
            self.tileSelection = [
                int(v) + (1 if i > 1 else 0) 
                for i, v in enumerate(self.raw_selection)
            ]
            self.selectionChanged.emit()
        else:
            self.rmbPressed = False
        self.scene().update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.RightButton:
            self.rmbPrevPos = [event.x(), event.y()]
            self.rmbPressed = True
        elif event.buttons() == QtCore.Qt.LeftButton:
            self.lmbPressed = True
            self.mouseCurX = self.mouseStartX = event.x()
            self.mouseCurY = self.mouseStartY = event.y()

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.rmbPressed:
            self.offsetX += event.x() - self.rmbPrevPos[0]
            self.offsetY += event.y() - self.rmbPrevPos[1]
            self.rmbPrevPos = [event.x(), event.y()]
            self.scene().update()
        elif self.lmbPressed:
            self.mouseCurX = event.x()
            self.mouseCurY = event.y()
            self.scene().update()

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.resetTransform()
        painter.fillRect(0, 0, self.size().width(), self.size().height(), QtGui.QColor('darkGray'))
        global_transform = QtGui.QTransform()
        global_transform.translate(self.offsetX, self.offsetY)
        painter.setTransform(global_transform, False)

        # Draw tile layer
        tile_layer = self.map.get_tile_layer()
        if tile_layer.visible:
            self.draw_tiles(tile_layer.data, painter, global_transform)
        # painter.scale(self.sc, self.sc)
        # Draw layer w/ objects
        for layer in self.map.get_object_layers(only_visible=True):
            self.draw_objects(layer.get_objects(), painter)

        painter.resetTransform()
        painter.setPen(QtGui.QColor('black'))
        if self.lmbPressed:
            painter.drawRect(0 + self.mouseStartX, 0 + self.mouseStartY
                             , self.mouseCurX - self.mouseStartX, self.mouseCurY - self.mouseStartY)

    def draw_tiles(self, layer_data, painter, global_transform):
        for y in range(len(layer_data)):
            for x in range(len(layer_data[y])):
                painter.scale(self.sc, self.sc)
                painter.translate(x * self.map.gridSize, y * self.map.gridSize)
                if layer_data[y][x].rotation == 90:
                    painter.rotate(90)
                    painter.translate(0, -self.map.gridSize)
                elif layer_data[y][x].rotation == 180:
                    painter.rotate(180)
                    painter.translate(-self.map.gridSize, -self.map.gridSize)
                elif layer_data[y][x].rotation == 270:
                    painter.rotate(270)
                    painter.translate(-self.map.gridSize, 0)
                painter.drawImage(QtCore.QRectF(0, 0, self.map.gridSize, self.map.gridSize),
                                  self.tileSprites[layer_data[y][x].kind])
                if self.tileSelection[0] <= x < self.tileSelection[2] and self.tileSelection[1] <= y < \
                        self.tileSelection[3]:
                    painter.setPen(QtGui.QColor('green'))
                    painter.drawRect(QtCore.QRectF(1, 1, self.map.gridSize - 1, self.map.gridSize - 1))
                else:
                    painter.setPen(QtGui.QColor('white'))
                    painter.drawRect(QtCore.QRectF(0, 0, self.map.gridSize, self.map.gridSize))
                painter.setTransform(global_transform, False)

    def draw_objects(self, layer_data, painter):
        for layer_object in layer_data:
            painter.drawImage(
                QtCore.QRectF(self.map.gridSize * self.sc * layer_object.position['x'],
                              self.map.gridSize * self.sc * layer_object.position['y'],
                              self.map.gridSize * self.sc / 2, self.map.gridSize * self.sc / 2),
                self.objects[layer_object.kind]) if layer_object.kind in self.objects else None
