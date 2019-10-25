# TODO тут будет вся работа с файлами
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from map_parser import *


def open_map(parent: QtWidgets.QWidget):
    input_map = QFileDialog.getOpenFileName(parent, 'Open file', '.')[0]
    parent.tiles.tiles = get_tiles(input_map)
    objects_array = get_objects(input_map)
    parent.tiles.gridSize = 100*get_tile_size(input_map)
    print(parent.tiles.tiles)
    print(objects_array)
    print(parent.tiles.gridSize)
