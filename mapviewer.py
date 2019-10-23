from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtCore, QtGui, QtWidgets
from map import DuckietownMap
from maptile import MapTile


# Пока на карте только один элемент - для тестирования функций виевера


class MapViewer(QGraphicsView, QtWidgets.QWidget):
    tiles = None
    tileSprites = {'empty': QtGui.QImage()}
    offsetX = 0
    offsetY = 0
    sc = 1
    rmbPressed = False
    rmbPrevPos = [0, 0]

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

    def setTiles(self, tiles: DuckietownMap):
        print('tiles set')
        self.tiles = tiles
        tile = MapTile('curve_left', 0)
        self.tiles.items.insert(0, [])
        self.tiles.items[0].insert(0, tile)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        sf = 2 ** (event.angleDelta().y() / 240)
        if (self.sc < 0.5 and sf < 1) or (self.sc > 100 and sf > 1):
            return
        self.sc *= sf
        self.scale(self.sc, self.sc)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        self.rmbPressed = False

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.buttons() == QtCore.Qt.RightButton:
            self.rmbPrevPos = [event.x(), event.y()]
            self.rmbPressed = True

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.rmbPressed:
            self.offsetX += event.x() - self.rmbPrevPos[0]
            self.offsetY += event.y() - self.rmbPrevPos[1]
            self.rmbPrevPos = [event.x(), event.y()]
            self.scene().update()

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        painter.fillRect(-700, -700, 1400, 1400, QtGui.QColor('white'))
        globalTransform = QtGui.QTransform()
        globalTransform.translate(self.offsetX, self.offsetY)
        painter.setTransform(globalTransform, False)
        for y in range(len(self.tiles.items)):
            for x in range(len(self.tiles.items[y])):
                painter.translate(x * self.tiles.gridSize, y * self.tiles.gridSize)
                if self.tiles.items[y][x].rotation == 90:
                    painter.rotate(90)
                    painter.translate(0, -self.tiles.gridSize)
                elif self.tiles.items[y][x].rotation == 180:
                    painter.rotate(180)
                    painter.translate(-self.tiles.gridSize, -self.tiles.gridSize)
                elif self.tiles.items[y][x].rotation == 270:
                    painter.rotate(270)
                    painter.translate(-self.tiles.gridSize, 0)
                painter.scale(self.sc, self.sc)
                painter.drawImage(QtCore.QRectF(0, 0, self.tiles.gridSize, self.tiles.gridSize),
                                  self.tileSprites[self.tiles.items[y][x].kind])
                painter.setTransform(globalTransform, False)
