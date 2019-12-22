class MapObject:

    #position = {'x': 0, 'y': 0}
    def __init__(self, kind, position, rotation, height, optional, static):
        self.kind = kind
        self.position = {}
        self.position['x'], self.position['y'] = position
        self.rotation = rotation
        self.height = height
        self.optional = optional
        self.static = static
