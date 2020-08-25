# -*- coding: utf-8 -*-
import unittest
import numpy as np

from map_parser import *
from maptile import MapTile
from mapobject import MapObject
from map import DuckietownMap


class TestMapParser(unittest.TestCase):

    def test_empty_map_objects(self):
        objects_array = get_objects('../maps/small_loop.yaml')
        self.assertEqual(objects_array, None)

    def test_tile_size(self):
        tile_size = data_from_file('../maps/small_loop.yaml').get('tile_size')
        self.assertEqual(tile_size, 0.585)

    def test_tiles_to_objects(self):
        tiles_objects_array = tiles_to_objects(get_tiles('../maps/test.yaml'))
        new_tiles_objects_array = [[MapTile('curve_left', 180), MapTile('straight', 180)],
                                   [MapTile('straight', 90), MapTile('asphalt', 0)]]
        for tile, new_tile in zip(np.array(tiles_objects_array).flat, np.array(new_tiles_objects_array).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

    def test_map_objects_to_objects(self):
        map_objects_array = map_objects_to_objects(get_objects('../maps/test.yaml'))
        objects_array = [MapObject('trafficlight', [2.2, 2.2], 45, 0.4, True, False)]
        for obj, new_obj in zip(map_objects_array, objects_array):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_1(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(get_tiles('../maps/regress_4way_adam.yaml')))
        map.set_item_layer(map_objects_to_objects(get_objects('../maps/regress_4way_adam.yaml')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(get_tiles('../maps/test_result.yaml')))
        new_map.set_item_layer(map_objects_to_objects(get_objects('../maps/test_result.yaml')))

        for tile, new_tile in zip(np.array(map.get_tile_layer()).flat, np.array(new_map.get_tile_layer()).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer(), new_map.get_item_layer()):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_2(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(get_tiles('../maps/test.yaml')))
        map.set_item_layer(map_objects_to_objects(get_objects('../maps/test.yaml')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(get_tiles('../maps/test_result.yaml')))
        new_map.set_item_layer(map_objects_to_objects(get_objects('../maps/test_result.yaml')))

        for tile, new_tile in zip(np.array(map.get_tile_layer()).flat, np.array(new_map.get_tile_layer()).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer(), new_map.get_item_layer()):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)

    def test_map_to_yaml_without_objects(self):

        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(get_tiles('../maps/regress_4way_drivable.yaml')))
        map.set_item_layer(map_objects_to_objects(get_objects('../maps/regress_4way_drivable.yaml')))

        map_to_yaml(map, '../maps/test_result.yaml')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(get_tiles('../maps/test_result.yaml')))
        new_map.set_item_layer(map_objects_to_objects(get_objects('../maps/test_result.yaml')))

        for tile, new_tile in zip(np.array(map.get_tile_layer()).flat, np.array(new_map.get_tile_layer()).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)
        self.assertEqual(map.get_item_layer(), new_map.get_item_layer())

    def test_map_to_yaml_without_yaml(self):
        map = DuckietownMap()
        map.set_tile_layer(tiles_to_objects(get_tiles('../maps/regress_4way_adam.yaml')))
        map.set_item_layer(map_objects_to_objects(get_objects('../maps/regress_4way_adam.yaml')))

        map_to_yaml(map, '../maps/test_result')

        new_map = DuckietownMap()
        new_map.set_tile_layer(tiles_to_objects(get_tiles('../maps/test_result.yaml')))
        new_map.set_item_layer(map_objects_to_objects(get_objects('../maps/test_result.yaml')))

        for tile, new_tile in zip(np.array(map.get_item_layer()).flat, np.array(new_map.get_item_layer()).flat):
            self.assertEqual(tile.kind, new_tile.kind)
            self.assertEqual(tile.rotation, new_tile.rotation)

        for obj, new_obj in zip(map.get_item_layer(), new_map.get_item_layer()):
            self.assertEqual(obj.kind, new_obj.kind)
            self.assertEqual(obj.position, new_obj.position)
            self.assertEqual(obj.rotation, new_obj.rotation)
            self.assertEqual(obj.height, new_obj.height)
            self.assertEqual(obj.optional, new_obj.optional)
            self.assertEqual(obj.static, new_obj.static)


if __name__ == '__main__':
    unittest.main()
