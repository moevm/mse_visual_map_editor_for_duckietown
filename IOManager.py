# TODO тут будет вся работа с файлами
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from map_parser import *


def open_map(self):
    input_map = QFileDialog.getOpenFileName(self, 'Open file', '.', filter=('YAML file (*.yaml)'))[0]
    tiles_array = get_tiles(input_map)
    objects_array = get_objects(input_map)
    tile_size = get_tile_size(input_map)
    print(tiles_array)
    print(objects_array)
    print(tile_size)
