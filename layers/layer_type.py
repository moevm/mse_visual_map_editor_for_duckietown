from enum import Enum


class LayerType(Enum):
    TILES = 'tiles'
    TRAFFIC_SIGNS = 'traffic_sings'
    GROUND_APRILTAG = 'ground_apriltag'
    WATCHTOWERS = 'watchtowers'
    REGIONS = 'regions'
    ITEMS = 'items'
