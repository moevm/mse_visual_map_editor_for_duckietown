import unittest
from map_parser import *
from maptile import MapTile
from mapobject import MapObject
from mapclass import Map


class TestMapParser(unittest.TestCase):

  def test_map_tiles(self):
      tiles_array = get_tiles('../maps/4way.yaml')
      result_tiles_array = [[{'kind': 'curve_left', 'rotate': 180}, {'kind': 'straight', 'rotate': 180}, {'kind': '3way_left', 'rotate': 180}, {'kind': 'straight', 'rotate': 180}, {'kind': 'curve_left', 'rotate': 270}],
                            [{'kind': 'straight', 'rotate': 90}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 270}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 270}],
                            [{'kind': '3way_left', 'rotate': 90}, {'kind': 'straight', 'rotate': 180}, {'kind': '4way', 'rotate': 0}, {'kind': 'straight', 'rotate': 0}, {'kind': '3way_left', 'rotate': 270}],
                            [{'kind': 'straight', 'rotate': 90}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 90}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 270}],
                            [{'kind': 'curve_left', 'rotate': 90}, {'kind': 'straight', 'rotate': 0}, {'kind': '3way_left', 'rotate': 0}, {'kind': 'straight', 'rotate': 0}, {'kind': 'curve_left', 'rotate': 0}]]
      self.assertEqual(tiles_array, result_tiles_array)

  def test_map_objects(self):
      objects_array = get_objects('../maps/4way.yaml')
      result_objects_array = [{'kind': 'trafficlight', 'pos': '[2.2,2.2]', 'rotate': '45', 'height': '0.4', 'optional': 'true', 'static':'True'}]
      self.assertEqual(objects_array, result_objects_array)

  def test_empty_map_objects(self):
      objects_array = get_objects('../maps/small_loop.yaml')
      self.assertEqual(objects_array, None)

  def test_tile_size(self):
      tile_size = get_tile_size('../maps/small_loop.yaml')
      self.assertEqual(tile_size, 0.585)

  def test_empty_file(self):
      tile_size = get_tile_size('urrr.yaml')
      self.assertEqual(tile_size, None)

  def test_tiles_to_objects(self):
      tiles_objects_array = tiles_to_objects(get_tiles('../maps/test.yaml'))
      tiles_array = []
      tiles_array.append([MapTile('curve_left', 180), MapTile('straight', 180)])
      tiles_array.append([MapTile('straight', 90),  MapTile('asphalt', 0)])
      for i in range(len(tiles_objects_array)):
          for j in range(len(tiles_objects_array[i])):
              self.assertEqual(tiles_objects_array[i][j].kind, tiles_array[i][j].kind)
              self.assertEqual(tiles_objects_array[i][j].rotation, tiles_array[i][j].rotation)


  def test_map_objects_to_objects(self):
      map_objects_array = map_objects_to_objects(get_objects('../maps/test.yaml'))
      objects_array = [MapObject('trafficlight', [2.2, 2.2], 45, 0.4, True, False)]
      for i in range(len(map_objects_array)):
          self.assertEqual(map_objects_array[i].kind, objects_array[i].kind)
          self.assertEqual(map_objects_array[i].position, objects_array[i].position)
          self.assertEqual(map_objects_array[i].rotation, objects_array[i].rotation)
          self.assertEqual(map_objects_array[i].height, objects_array[i].height)
          self.assertEqual(map_objects_array[i].optional, objects_array[i].optional)
          self.assertEqual(map_objects_array[i].static, objects_array[i].static)

  def test_map_to_yaml_1(self):
      map_objects_array = map_objects_to_objects(get_objects('../maps/regress_4way_adam.yaml'))
      tile_objects_array = tiles_to_objects(get_tiles('../maps/regress_4way_adam.yaml'))
      map = Map(tile_objects_array, map_objects_array)
      map_to_yaml(map, '../maps/test_result')
      new_map_objects_array = map_objects_to_objects(get_objects('../maps/test_result.yaml'))
      new_tile_objects_array = tiles_to_objects(get_tiles('../maps/test_result.yaml'))
      new_map = Map(new_tile_objects_array, new_map_objects_array)
      for i in range(len(map.tiles)):
          for j in range(len(map.tiles[i])):
              self.assertEqual(map.tiles[i][j].kind, new_map.tiles[i][j].kind)
              self.assertEqual(map.tiles[i][j].rotation, new_map.tiles[i][j].rotation)
      for i in range(len(map.objects)):
          self.assertEqual(map.objects[i].kind, new_map.objects[i].kind)
          self.assertEqual(map.objects[i].position, new_map.objects[i].position)
          self.assertEqual(map.objects[i].rotation, new_map.objects[i].rotation)
          self.assertEqual(map.objects[i].height, new_map.objects[i].height)
          self.assertEqual(map.objects[i].optional, new_map.objects[i].optional)
          self.assertEqual(map.objects[i].static, new_map.objects[i].static)


  def test_map_to_yaml_2(self):
      map_objects_array = map_objects_to_objects(get_objects('../maps/test.yaml'))
      tile_objects_array = tiles_to_objects(get_tiles('../maps/test.yaml'))
      map = Map(tile_objects_array, map_objects_array)
      map_to_yaml(map, '../maps/test_result')
      new_map_objects_array = map_objects_to_objects(get_objects('../maps/test_result.yaml'))
      new_tile_objects_array = tiles_to_objects(get_tiles('../maps/test_result.yaml'))
      new_map = Map(new_tile_objects_array, new_map_objects_array)
      for i in range(len(map.tiles)):
          for j in range(len(map.tiles[i])):
              self.assertEqual(map.tiles[i][j].kind, new_map.tiles[i][j].kind)
              self.assertEqual(map.tiles[i][j].rotation, new_map.tiles[i][j].rotation)
      for i in range(len(map.objects)):
          self.assertEqual(map.objects[i].kind, new_map.objects[i].kind)
          self.assertEqual(map.objects[i].position, new_map.objects[i].position)
          self.assertEqual(map.objects[i].rotation, new_map.objects[i].rotation)
          self.assertEqual(map.objects[i].height, new_map.objects[i].height)
          self.assertEqual(map.objects[i].optional, new_map.objects[i].optional)
          self.assertEqual(map.objects[i].static, new_map.objects[i].static)

  def test_map_to_yaml_without_objects(self):
      map_objects_array = map_objects_to_objects(get_objects('../maps/regress_4way_drivable.yaml'))
      tile_objects_array = tiles_to_objects(get_tiles('../maps/regress_4way_drivable.yaml'))
      map = Map(tile_objects_array, map_objects_array)
      map_to_yaml(map, '../maps/test_result')
      new_map_objects_array = map_objects_to_objects(get_objects('../maps/test_result.yaml'))
      new_tile_objects_array = tiles_to_objects(get_tiles('../maps/test_result.yaml'))
      new_map = Map(new_tile_objects_array, new_map_objects_array)
      for i in range(len(map.tiles)):
          for j in range(len(map.tiles[i])):
              self.assertEqual(map.tiles[i][j].kind, new_map.tiles[i][j].kind)
              self.assertEqual(map.tiles[i][j].rotation, new_map.tiles[i][j].rotation)
      self.assertEqual(map.objects, new_map.objects)



if __name__ == '__main__':
    unittest.main()
