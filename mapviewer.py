from PyQt5.QtWidgets import QGraphicsView
from PyQt5 import QtCore, QtGui, QtWidgets
from map import DuckietownMap


class MapViewer(QGraphicsView, QtWidgets.QWidget):
    tiles = 0

    def __init__(self, parent=None):
        print('viewer created')
        QGraphicsView.__init__(self)

    def setTiles(self, tiles: DuckietownMap):
        print('tiles set')
        self.tiles = tiles

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF):
        print('viewer rendered')
        painter.setPen(QtGui.QColor("red"))
        painter.fillRect(0,0,100,100)
        return
