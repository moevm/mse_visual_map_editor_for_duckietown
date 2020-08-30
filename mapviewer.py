# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtCore, QtGui, QtWidgets
from map import DuckietownMap

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
        self.tileSprites['empty'].load('./img/tiles/empty.png')
        self.tileSprites['straight'] = QtGui.QImage()
        self.tileSprites['straight'].load('./img/tiles/straight.png')
        self.tileSprites['curve_left'] = QtGui.QImage()
        self.tileSprites['curve_left'].load('./img/tiles/curve_left.png')
        self.tileSprites['curve_right'] = QtGui.QImage()
        self.tileSprites['curve_right'].load('./img/tiles/curve_right.png')
        self.tileSprites['3way_left'] = QtGui.QImage()
        self.tileSprites['3way_left'].load('./img/tiles/three_way_left.png')
        self.tileSprites['3way_right'] = QtGui.QImage()
        self.tileSprites['3way_right'].load('./img/tiles/three_way_right.png')
        self.tileSprites['4way'] = QtGui.QImage()
        self.tileSprites['4way'].load('./img/tiles/four_way_center.png')
        self.tileSprites['asphalt'] = QtGui.QImage()
        self.tileSprites['asphalt'].load('./img/tiles/asphalt.png')
        self.tileSprites['grass'] = QtGui.QImage()
        self.tileSprites['grass'].load('./img/tiles/grass.png')
        self.tileSprites['floor'] = QtGui.QImage()
        self.tileSprites['floor'].load('./img/tiles/floor.png')

        # watchtower
        self.objects['watchtower'] = QtGui.QImage()
        self.objects['watchtower'].load('./img/objects/watchtower.png')

        sign_names = ['sign_stop', 'sign_yield', 'sign_no_right_turn', 'sign_no_left_turn', 'sign_do_not_enter',
                      'sign_oneway_right', 'sign_oneway_left', 'sign_4_way_intersect', 'sign_right_T_intersect',
                      'sign_left_T_intersect', 'sign_T_intersection', 'sign_pedestrian', 'sign_t_light_ahead',
                      'sign_duck_crossing', 'sign_parking']
        for t in sign_names:
            self.objects[t] = QtGui.QImage()
            self.objects[t].load('./img/signs/' + t + '.png')
        items = ["trafficlight", "barrier", "cone", "duckie", "duckiebot", 'tree', "house", "truck", "bus",
                 "building", ]
        for o in items:
            self.objects[o] = QtGui.QImage()
            self.objects[o].load('./img/objects/' + o + '.png')

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
        print(layer_data)
        for layer_object in layer_data:
            print(layer_object.kind)
            print(layer_object.position)
            print(layer_object.kind in self.objects)
            print(self.objects[layer_object.kind])
            painter.drawImage(
                QtCore.QRectF(self.map.gridSize * self.sc * layer_object.position['x'],
                              self.map.gridSize * self.sc * layer_object.position['y'],
                              self.map.gridSize * self.sc / 2, self.map.gridSize * self.sc / 2),
                self.objects[layer_object.kind]) if layer_object.kind in self.objects else None
