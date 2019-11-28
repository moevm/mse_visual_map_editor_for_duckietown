# TODO тут будет вся работа с файлами
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from map_parser import *


def open_map(parent: QtWidgets.QWidget):
    input_map = QFileDialog.getOpenFileName(parent, 'Open file', '.', filter=('YAML file (*.yaml)'))[0]
    if input_map:
        parent.map.name = input_map
        parent.map.tiles = tiles_to_objects(get_tiles(input_map))
        parent.map.items = map_objects_to_objects(get_objects(input_map))
        parent.map.gridSize = 100*get_tile_size(input_map)
    # map_to_png(parent.map, 'opp.png')


def save_map_as(parent: QtWidgets.QWidget):
    if len(parent.map.tiles) > 0:
        output_map = QFileDialog.getSaveFileName(parent, 'Save file', '.', filter=('YAML file (*.yaml)'))[0]
        if output_map:
            map_to_yaml(parent.map, output_map)

def save_map(parent: QtWidgets.QWidget):
    if len(parent.map.tiles) > 0:
        map_to_yaml(parent.map, parent.map.name)

def export_png(parent: QtWidgets.QWidget):
    if len(parent.map.tiles) > 0:
        output_map = QFileDialog.getSaveFileName(parent, 'Save file', '.', filter=('PNG file (*.png)'))[0]
        if output_map:
            map_to_png(parent.map, output_map)