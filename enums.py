from enum import Enum

class CoordsType(Enum):
    BLENDER = "Blender"
    COLMAP = "COLMAP"

class TransformType(Enum):
    C2W = "c2w"
    W2C = "w2c"