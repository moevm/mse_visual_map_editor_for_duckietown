from enum import Enum


class LayerType(Enum):
    TILES = 'tiles'
    TRAFFIC_SIGNS = 'traffic_sings'
    GROUND_APRILTAG = 'ground_apriltag'
    WATCHTOWERS = 'watchtowers'
    REGIONS = 'regions'
    ITEMS = 'items'

    def __str__(self):
        return self.value


LAYER_TYPE_WITH_OBJECTS = (LayerType.TRAFFIC_SIGNS, LayerType.GROUND_APRILTAG, LayerType.WATCHTOWERS, LayerType.ITEMS)
