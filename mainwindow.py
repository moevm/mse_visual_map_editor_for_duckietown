from PyQt5 import QtWidgets
# import design
import mapviewer
import map
from PyQt5 import QtWidgets, QtGui


class ExampleApp(QtWidgets.QMainWindow):
    tiles = None

    def __init__(self):
        super().__init__()
        self.tiles = map.DuckietownMap()
        # self.setupUi(self)
        hwidget = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(hwidget)
        viewer = mapviewer.MapViewer(hwidget)
        viewer.setTiles(self.tiles)
        viewer.setMinimumSize(400, 400)
        label = QtWidgets.QLabel("тут панель плитки", hwidget)
        layout.addWidget(viewer)
        layout.addWidget(label)
        hwidget.setLayout(layout)
        self.setCentralWidget(hwidget)
        self.setMinimumSize(640, 480)
        viewer.repaint()
        # сраный qt не дает нарисовать виевер