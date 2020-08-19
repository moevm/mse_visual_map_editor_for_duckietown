# -*- coding: utf-8 -*-
TILE_LAYER_NAME = "tiles"
ITEM_LAYER_NAME = "items"


class DuckietownMap:
    name = None
    gridSize = 58.5

    def __init__(self):
        # default layers
        self.layer_list = [TILE_LAYER_NAME, ITEM_LAYER_NAME]
        self.layer_info = {
            TILE_LAYER_NAME: [[]],
            ITEM_LAYER_NAME: []
        }

    # Getters

    def get_tile_layer(self):
        """
        Get tile layer's data (default name define by TILE_LAYER_NAME)
        :return: list(list)
        """
        return self.get_layer(TILE_LAYER_NAME)

    def get_item_layer(self):
        """
        Get item layer's data (default name define by ITEM_LAYER_NAME)
        :return: list
        """
        return self.get_layer(ITEM_LAYER_NAME)

    def get_layer(self, name):
        """
        Get layer's data by name
        :param name: name of layer
        :return: list, if name doesn't exist, return None
        """
        return self.layer_info.get(name, [])

    # Setters

    def set_tile_layer(self, layer):
        """
        Set tile layer's data
        :param layer: list(list)
        :return: -
        """
        self.set_layer(TILE_LAYER_NAME, layer)

    def set_item_layer(self, layer):
        """
        Set item layer's data
        :param layer: list
        :return: -
        """
        self.set_layer(ITEM_LAYER_NAME, layer)

    def set_layer(self, name, layer):
        """
        Set layer's data by name
        :param name: layer's name
        :param layer: list
        :return: -
        """
        self.layer_info[name] = layer
        if name not in self.layer_list:  # for adding new layers in future
            self.layer_list.append(name)
