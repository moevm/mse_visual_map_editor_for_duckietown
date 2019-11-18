class MapObject:
    kind = 'empty'
    position = [0, 0]
    rotation = 0
    height = 0
    optional = False
    static = False

    def __init__(self, kind, position, rotation, height, optional, static):
        self.kind = kind
        self.position[0] = position[0]
        self.position[1] = position[1]
        self.rotation = rotation
        self.height = height
        self.optional = optional
        self.static = static
