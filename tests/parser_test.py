import unittest
from map_parser import get_tiles, get_objects, get_tile_size

class TestMapParser(unittest.TestCase):

  def test_map_tiles(self):
      tiles_array = get_tiles('../maps/4way.yaml')
      result_tiles_array = [[{'kind': 'curve_left', 'rotate': 270}, {'kind': 'straight', 'rotate': 270}, {'kind': '3way_left', 'rotate': 270}, {'kind': 'straight', 'rotate': 270}, {'kind': 'curve_left', 'rotate': 0}], [{'kind': 'straight', 'rotate': 180}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 0}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 0}], [{'kind': '3way_left', 'rotate': 180}, {'kind': 'straight', 'rotate': 270}, {'kind': '4way', 'rotate': 0}, {'kind': 'straight', 'rotate': 90}, {'kind': '3way_left', 'rotate': 0}], [{'kind': 'straight', 'rotate': 180}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 180}, {'kind': 'asphalt', 'rotate': 0}, {'kind': 'straight', 'rotate': 0}], [{'kind': 'curve_left', 'rotate': 180}, {'kind': 'straight', 'rotate': 90}, {'kind': '3way_left', 'rotate': 90}, {'kind': 'straight', 'rotate': 90}, {'kind': 'curve_left', 'rotate': 90}]]
      self.assertEqual(tiles_array, result_tiles_array)

  def test_map_objects(self):
      objects_array = get_objects('../maps/4way.yaml')
      result_objects_array = [{'kind': 'trafficlight', 'pos': '[2.2,2.2]', 'rotate': '45', 'height': '0.4', 'optional': 'true'}]
      self.assertEqual(objects_array, result_objects_array)

  def test_empty_map_objects(self):
      objects_array = get_objects('../maps/small_loop.yaml')
      self.assertEqual(objects_array, None)

  def test_tile_size(self):
      tile_size = get_tile_size('../maps/small_loop.yaml')
      self.assertEqual(tile_size, 0.585)

if __name__ == '__main__':
    unittest.main()
