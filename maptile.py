class MapTile:
    kind = 'empty'
    # pos = {'x': 0, 'y': 0}
    rotation = 0

    # height = 0
    # static = True
    def __init__(self, kind, rotation):
        self.kind = kind
        self.rotation = rotation
