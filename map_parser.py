import re


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
                if rotate == 'N':
                    tile_object['rotate'] = 0
                elif rotate == 'E':
                    tile_object['rotate'] = 90
                elif rotate == 'S':
                    tile_object['rotate'] = 180
                elif rotate == 'W':
                    tile_object['rotate'] = 270
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
