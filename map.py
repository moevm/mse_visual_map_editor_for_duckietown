# -*- coding: utf-8 -*-
from layers.map_layer import MapLayer
from layers.layer_type import LayerType

import logging

logger = logging.getLogger('root')


class DuckietownMap:
    name = None
    gridSize = 58.5

    def __init__(self, empty=False):
        self.layers = [MapLayer(LayerType.TILES, [[]]), MapLayer(LayerType.ITEMS, [])] if not empty else []

    # Getters

    def get_tile_layer(self):
        """
        Get tile layer's data (default name define by TILE_LAYER_NAME)
        :return: list(list)
        """
        return self.get_layer_by_type(LayerType.TILES)

    def get_item_layer(self):
        """
        Get item layer's data (default name define by ITEM_LAYER_NAME)
        If item layer doesn't exist, function create it
        :return: list
        """
        layer = self.get_layer_by_type(LayerType.ITEMS)
        if layer is None:  # if layer doesn't exist, layer = None
            layer = []
            self.add_layer_from_data(LayerType.ITEMS, layer)
        return layer

    def get_layer_by_name(self, name):
        """
        Get layer by name
        :param name: name of layer
        :return: list, if name doesn't exist, return None
        """
        for layer in self.layers:
            if layer.name == name:
                return layer
        return None

    def get_layer_by_type(self, layer_type: LayerType):
        """
        Get layer by type
        :param layer_type: type of layer
        :return: list, if layer w/ type doesn't exist, return None
        """
        for layer in self.layers:
            if layer.type == layer_type:
                return layer
        return None

    # Setters

    def set_tile_layer(self, layer: list):
        """
        Set tile layer's data
        :param layer: list(list)
        :return: bool, return False if layer doesn't exist, else True
        """
        self.set_layer_data_by_type(LayerType.TILES, layer)

    def set_item_layer(self, layer: list):
        """
        Set item layer's data
        :param layer: list
        :return: bool, return False if layer doesn't exist, else True
        """
        self.set_layer_data_by_type(LayerType.ITEMS, layer)

    def set_layer_data_by_name(self, layer_name: str, layer_data: list):
        """
        Set layer's data by name
        :param layer_name: name of layer
        :param layer_data: list
        :return: bool, return False if layer doesn't exist, else True
        """
        layer = self.get_layer_by_name(layer_name)
        if layer:
            return self.set_layer_data_by_type(layer.type, layer_data)
        else:
            logger.info("Layer with name '{}' doesn't exist".format(layer_name))
            return False

    def set_layer_data_by_type(self, layer_type: LayerType, layer_data: list):
        """
        Set layer's data by name
        :param layer_type: type of layer
        :param layer_data: list
        :return: bool, return False if layer doesn't exist, else True
        """
        layer = self.get_layer_by_type(layer_type)
        if layer:
            layer.data = layer_data
            return True
        else:
            logger.info("Layer with type '{}' doesn't exist".format(layer_type))
            return False

    def set_layer(self, new_layer: MapLayer):
        for i, layer in enumerate(self.layers):
            if layer.type == new_layer.type:
                self.layers[i] = new_layer
                return True
        logger.info("Layer with type '{}' doesn't exists. Can't set new layer".format(new_layer.type))

    # Creating layer

    def add_layer_from_data(self, layer_type: LayerType, layer_data=None, layer_name=''):
        """
        Add layer to map from layer_type and layer_data
        :param layer_type: LayerType
        :param layer_data: list
        :param layer_name: str
        :return: bool, return False, if layer with such LayerType already exists, else True
        """
        if self.get_layer_by_type(layer_type):
            logger.info("Layer with type '{}' already exists.\nTo set new layer data use "
                        "set_layer_data/set_layer_data_by_type.\nTo set new layer name use "
                        "set_layer_name/set_layer_name_by_type".format(layer_type))
            return False
        else:
            return self.add_layer(MapLayer(layer_type, layer_data if layer_data else [], layer_name))

    def add_layer(self, layer: MapLayer):
        """
        Add layer to map
        :param layer: MapLayer
        :return: bool, return False, if layer with such LayerType already exists, else True
        """
        if self.get_layer_by_type(layer.type):
            logger.info("Layer with type '{}' already exists.\nTo set new layer data use "
                        "set_layer_data/set_layer_data_by_type.\nTo set new layer name use "
                        "set_layer_name/set_layer_name_by_type".format(layer.type))
            return False
        else:
            self.layers.append(layer)
            return True

    # Adding elem to layers

    def add_item(self, item):
        """
        Add item to item layer (default name define by ITEM_LAYER_NAME)
        :param item: MapObject. Note: after adding specific layers, it can change
        :return: bool (looks like it always True)
        """
        return self.add_elem_to_layer_by_type(LayerType.ITEMS, item)

    def add_elem_to_layer(self, layer_name: str, elem):
        """
        Add elem to layer by name
        (Doesn't add elements to tile_layer due to different structure)
        :param layer_name: name of layer
        :param elem: MapObject. Note: after adding specific layers, it can change
        :return: bool, return False if layer doesn't exist, else True
        """
        layer = self.get_layer_by_name(layer_name).type
        if layer is not None:
            return self.add_elem_to_layer_by_type(layer.type, elem)
        else:
            logger.info("Layer with name '{}' doesn't exist".format(layer_name))
            return False

    def add_elem_to_layer_by_type(self, layer_type: LayerType, elem):
        """
        Add elem to layer by type
        (Doesn't add elements to tile_layer due to different structure)
        :param layer_type: type of layer
        :param elem: MapObject. Note: after adding specific layers, it can change
        :return: bool, return False if layer doesn't exist, else True
        """
        if layer_type == LayerType.TILES:
            logger.warning("Don't use this method for tile layer.")
            return False
        layer = self.get_layer_by_type(layer_type)
        if layer is not None:  # layer can exist, but be empty. get_layer_by_name/get_layer_by_type return None, if layer doesn't exist
            layer.add_elem(elem)
            return True
        else:
            logger.info("Layer with type '{}' doesn't exist".format(layer_type))
            return False
