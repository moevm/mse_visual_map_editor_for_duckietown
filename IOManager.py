# TODO тут будет вся работа с файлами
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from map_parser import *
from mapclass import Map



def open_map(parent: QtWidgets.QWidget):
    input_map = QFileDialog.getOpenFileName(parent, 'Open file', '.', filter=('YAML file (*.yaml)'))[0]

    map = Map(tiles_to_objects(get_tiles(input_map)),  map_objects_to_objects(get_objects(input_map)))
    parent.tiles.tiles = map.tiles

    parent.tiles.gridSize = 100*get_tile_size(input_map)
    print(parent.tiles.tiles)
    print(parent.tiles.gridSize)
