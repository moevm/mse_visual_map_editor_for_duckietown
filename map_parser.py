import re
from maptile import MapTile
from mapobject import MapObject

rotation_val = {0: 'E', 90: 'S', 180: 'W', 270: 'N'}


def map_to_yaml(map, map_name):
    f = open(map_name + '.yaml', 'w')
    f.write('tiles:\n')
    for tile_string in map.tiles:
        f.write('- [')
        for tile in tile_string:
            f.write(tile.kind)
            if tile.rotation == 0:
                if tile.kind != 'asphalt' and tile.kind != 'grass' and tile.kind != 'floor' and tile.kind != '4way':
                    f.write('/E')
            else:
                f.write('/' + rotation_val[tile.rotation])
            if tile_string.index(tile) != len(tile_string) - 1:
                f.write(' , ')
        f.write(']\n')
    if map.objects is not None:
        f.write('\nobjects:')
        for map_object in map.objects:
            f.write('\n- ')
            f.write('kind: ' + map_object.kind)
            f.write('\n  pos: [' + str(map_object.position['x']) + ', ' + str(map_object.position['y']) + ']')
            f.write('\n  rotate: ' + str(map_object.rotation))
            f.write('\n  height: ' + str(map_object.height))
            if map_object.optional:
                f.write('\n  optional: true')
            if not map_object.static:
                f.write('\n  static: False')
            f.write('\n')
    f.write('\ntile_size: 0.585')
    f.close()


def tiles_to_objects(tiles):
    tiles_objects_array = []
    for tile_string in tiles:
        tiles_object_string = []
        for tile in tile_string:
            tiles_object_string.append(MapTile(tile['kind'], tile['rotate']))
        tiles_objects_array.append(tiles_object_string)
    return tiles_objects_array


def map_objects_to_objects(map_objects):
    map_objects_array = []
    if not map_objects:
        return None
    for object in map_objects:
        x, y = re.sub(r"[\[\]]", "", object['pos']).split(',')
        position = [float(x), float(y)]
        rotation = float(object['rotate'])
        height = float(object['height'])
        optional = True if object['optional'] == 'true' else False
        static = True if object['static'] == 'True' else False
        map_objects_array.append(MapObject(object['kind'], position, rotation, height, optional, static))
    return map_objects_array


def get_tiles(name):
    tiles_array = []
    try:
        f = open(name, 'r')
    except IOError:
        print("Could not open file!")
        return None

    while True:
        map_line = f.readline()
        if 'tiles:' in map_line != -1:
            break

    map_line = f.readline()
    while map_line[0] == '-':
        map_line = re.sub(r"[ \t\[\]\-\n]", "", map_line)
        tiles = map_line.split(',')

        tile_string = []
        for tile in tiles:
            tile_object = {}
            if '/' in tile != -1:
                kind, rotate = tile.split('/')
                tile_object['kind'] = kind
                for angle, word in rotation_val.items():
                    if word == rotate:
                        tile_object['rotate'] = angle
            else:
                tile_object['kind'] = tile
                tile_object['rotate'] = 0
            tile_string.append(tile_object)
        tiles_array.append(tile_string)
        map_line = f.readline()

    f.close()
    return tiles_array


def get_objects(name):
    objects_array = []
    try:
        f = open(name, 'r')
    except IOError:
        print("Could not open file!")
        return None

    map_line = f.readline()
    while map_line:
        if 'objects:' in map_line != -1:
            break
        map_line = f.readline()

    if not map_line:
        f.close()
        return None

    while map_line[0] != 't':
        if map_line[0] == '-':
            map_object = {}
            while True:
                map_line = re.sub(r"[ \t\n-]", "", map_line)
                splits_line = map_line.split(':')
                map_object[splits_line[0]] = splits_line[1]
                map_line = f.readline()

                if map_line[0] == '-' or map_line[0] == 't' or map_line[0] == "\n":
                    if 'optional' not in map_object:
                        map_object['optional'] = 'false'
                    if 'static' not in map_object:
                        map_object['static'] = 'True'
                    objects_array.append(map_object)
                    break
        else:
            map_line = f.readline()
    f.close()
    return objects_array


def get_tile_size(name):
    try:
        f = open(name, 'r')
    except IOError:
        print("Could not open file!")
        return None

    while True:
        map_line = f.readline()
        if 'tile_size:' in map_line != -1:
            break
    map_line = map_line.split(':')

    f.close()
    return float(map_line[1])
