from layers.layer_type import LayerType


class MapLayer:
    def __init__(self, layer_type: LayerType, layer_data: list, name=''):
        self.name = name if name else layer_type.value
        self.type = layer_type
        self.data = layer_data
        self.visible = True

    def add_elem(self, elem):
        self.data.append(elem)

    def to_dict(self):
        return {
            'name': self.name,
            'type': self.type,
            'data': self.data,
            'visible': self.visible
        }
