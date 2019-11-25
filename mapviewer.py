from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtCore, QtGui, QtWidgets
from map import DuckietownMap
from maptile import MapTile


class MapViewer(QGraphicsView, QtWidgets.QWidget):
    tiles = None
    tileSprites = {'empty': QtGui.QImage()}
    offsetX = 0
    offsetY = 0
    sc = 1
    rmbPressed = False
    lmbPressed = False
    rmbPrevPos = [0, 0]
    mouseStartX, mouseStartY = 0, 0
    mouseCurX, mouseCurY = 0, 0
    tileSelection = [0] * 4
    selectionChanged = QtCore.pyqtSignal()# Сигнал TODO

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
        self.tileSprites['3way_right'].load('./img/tiles/three_way_left.png')
        self.tileSprites['4way'] = QtGui.QImage()
        self.tileSprites['4way'].load('./img/tiles/four_way_center.png')
        self.tileSprites['asphalt'] = QtGui.QImage()
        self.tileSprites['asphalt'].load('./img/tiles/asphalt.png')
        self.tileSprites['grass'] = QtGui.QImage()
        self.tileSprites['grass'].load('./img/tiles/grass.png')
        self.tileSprites['floor'] = QtGui.QImage()
        self.tileSprites['floor'].load('./img/tiles/floor.png')

    def setMap(self, tiles: DuckietownMap):
        self.tiles = tiles
        self.tileSelection = [0]*4
        self.scene().update()

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        sf = 2 ** (event.angleDelta().y() / 240)
        if (self.sc < 0.5 and sf < 1) or (self.sc > 100 and sf > 1):
            return
        self.sc *= sf
        self.scene().update()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.LeftButton:
            print(event.x(), event.y())
        self.rmbPressed = False
        self.lmbPressed = False
        self.tileSelection[0] = int(max((min(self.mouseStartX, self.mouseCurX) - self.offsetX) / self.sc
                                        , 0) / self.tiles.gridSize)
        self.tileSelection[1] = int(max((min(self.mouseStartY, self.mouseCurY) - self.offsetY) / self.sc
                                        , 0) / self.tiles.gridSize)
        self.tileSelection[2] = int(((max(self.mouseStartX, self.mouseCurX) - self.offsetX) / self.sc) / self.tiles.gridSize)
        self.tileSelection[3] = int(((max(self.mouseStartY, self.mouseCurY) - self.offsetY) / self.sc) / self.tiles.gridSize)
        print(self.tileSelection)
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
        painter.fillRect(-2000, -1000, 4000, 2000, QtGui.QColor('darkGray'))
        globalTransform = QtGui.QTransform()
        globalTransform.translate(self.offsetX, self.offsetY)
        painter.setTransform(globalTransform, False)
        for y in range(len(self.tiles.tiles)):
            for x in range(len(self.tiles.tiles[y])):
                painter.scale(self.sc, self.sc)
                painter.translate(x * self.tiles.gridSize, y * self.tiles.gridSize)
                if self.tiles.tiles[y][x].rotation == 90:
                    painter.rotate(90)
                    painter.translate(0, -self.tiles.gridSize)
                elif self.tiles.tiles[y][x].rotation == 180:
                    painter.rotate(180)
                    painter.translate(-self.tiles.gridSize, -self.tiles.gridSize)
                elif self.tiles.tiles[y][x].rotation == 270:
                    painter.rotate(270)
                    painter.translate(-self.tiles.gridSize, 0)
                painter.drawImage(QtCore.QRectF(0, 0, self.tiles.gridSize, self.tiles.gridSize),
                                  self.tileSprites[self.tiles.tiles[y][x].kind])
                if self.tileSelection[0] <= x < self.tileSelection[2] and self.tileSelection[1] <= y < \
                        self.tileSelection[3]:
                    painter.setPen(QtGui.QColor('green'))
                    painter.drawRect(QtCore.QRectF(1, 1, self.tiles.gridSize-1, self.tiles.gridSize-1))
                else:
                    painter.setPen(QtGui.QColor('white'))
                    painter.drawRect(QtCore.QRectF(0, 0, self.tiles.gridSize, self.tiles.gridSize))
                painter.setTransform(globalTransform, False)
        painter.resetTransform()
        painter.setPen(QtGui.QColor('black'))
        if self.lmbPressed:
            painter.drawRect(0 + self.mouseStartX, 0 + self.mouseStartY
                             , self.mouseCurX - self.mouseStartX, self.mouseCurY - self.mouseStartY)
