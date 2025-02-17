import bpy
from dataclasses import dataclass
import numpy as np
from .enums import CoordsType, TransformType
from .read_write_model import qvec2rotmat, rotmat2qvec

# def to4d(R, T):
#     W = np.zeros((4, 4))
#     W[3, 3] = 1
#     W[:3, :3] = R
#     W[:3, 3] = T
#     return W

@dataclass
class Intrinsics:
    id: int
    width: int
    height: int
    model: str
    fx: float
    fy: float
    cx: float
    cy: float
    k: list[int | None]
    p1: float | None
    p2: float | None

    @classmethod
    def frommodel(cls, id, width, height, model, params):
        f, fx, fy, cx, cy, k1, k2, p1, p2, k3, k4, k5, k6 = [None] * 13
        match model:
            case 'SIMPLE_PINHOLE':
                f, cx, cy = params
            case 'PINHOLE':
                fx, fy, cx, cy = params
            case 'SIMPLE_RADIAL':
                f, cx, cy, k = params
            case 'RADIAL':
                f, cx, cy, k1, k2 = params
            case 'OPENCV':
                fx, fy, cx, cy, k1, k2, p1, p2 = params
            case 'FULL_OPENCV':
                fx, fy, cx, cy, k1, k2, p1, p2, k3, k4, k5, k6 = params
            case 'SIMPLE_RADIAL_FISHEYE':
                f, cx, cy, k = params
            case 'RADIAL_FISHEYE':
                f, cx, cy, k1, k2 = params
            case 'OPENCV_FISHEYE':
                fx, fy, cx, cy, k1, k2, k3, k4 = params
            case _:
                raise ValueError(f"Unsupported Camera Model: {model}")
        if f is not None:
            fx = fy = f
        if k is not None:
            k1 = k2 = k
        ks = [k1, k2, k3, k4, k5, k6]
        return cls(id, width, height, model, fx, fy, cx, cy, ks, p1, p2)
    
@dataclass
class Extrinsics:
    id: int
    qvec: np.ndarray
    tvec: np.ndarray
    matrix: np.ndarray
    camera_id: int
    name: str
    points2d: np.ndarray | None

    @classmethod
    def fromquat(cls, id, qvec, tvec, cam_id, name, points2d=None):
        matrix = np.zeros((4, 4))
        matrix[3, 3] = 1
        matrix[:3, :3] = qvec2rotmat(qvec)
        matrix[:3, 3] = tvec
        return cls(id, qvec, tvec, matrix, cam_id, name, points2d)

    @classmethod
    def frommarix(cls, id, matrix, cam_id, name):
        qvec = rotmat2qvec(matrix[:3, :3])
        tvec = matrix[:3, 3]
        return cls(id, qvec, tvec, matrix, cam_id, name, None)



class BCamera:
    def __init__(self, intr, extr):
        self._intr = intr
        self._extr = extr
    
    @property
    def img_width(self):
        return self._intr.width
    
    @property
    def img_height(self):
        return self._intr.height
    
    @property
    def camera_model(self):
        return self._intr.model

    @property
    def matrix(self):
        return self._extr.matrix
    
    @property
    def qvec(self):
        return self._extr.qvec
    
    @property
    def tvec(self):
        return self._extr.tvec
    
    @property
    def R(self):
        return self._extr.matrix[:3, :3]
    
    @property
    def T(self):
        return self._extr.matrix[:3, 3]
    


@dataclass
class Camera:
    width: int
    height: int
    image_path: str
    R: np.ndarray
    T: np.ndarray
    params: np.ndarray
    camera_type: str
    transform_type: TransformType = TransformType.W2C
    coords_type: CoordsType = CoordsType.COLMAP

    # Define a post initialization method
    def __post_init__(self):
        # Automatically calculate w2c and c2w when the camera is created
        params = self.params
        type_ = self.camera_type
        if type_ == 0 or type_ == 'SIMPLE_PINHOLE':
            self.fx, self.cx, self.cy = params
            self.fy = self.fx
            self.camera_type = 0
        elif type_ == 1 or type_ == 'PINHOLE':
            self.fx, self.fy, self.cx, self.cy = params
            self.camera_type = 1
        elif type_ == 2 or type_ == 'SIMPLE_RADIAL':
            self.fx, self.cx, self.cy, self.k1 = params
            self.fy = self.fx
            self.camera_type = 2
        elif type_ == 3 or type_ == 'RADIAL':
            self.fx, self.cx, self.cy, self.k1, self.k2 = params
            self.fy = self.fx
            self.camera_type = 3
        elif type_ == 4 or type_ == 'OPENCV':
            self.fx, self.fy, self.cx, self.cy = params[:4]
            self.k1, self.k2, self.p1, self.p2 = params[4:]
            self.camera_type = 4
        else:
            raise Exception('Camera type not supported')

    def to(self, new_type: TransformType):
        if self.transform_type != new_type:
            R = self.R.T
            T = -R @ self.T
            self.R = R
            self.T = T
        return self

    @property
    def M(self):
        return to4d(self.R, self.T)

    def astype(self, new_type: CoordsType):
        """Convert between COLMAP and Blender coordinate systems."""
        if self.coords_type == new_type:
            return self

        R, T = self.R.copy(), self.T.copy()
        if (new_type == CoordsType.BLENDER and self.coords_type == CoordsType.COLMAP) or (new_type == CoordsType.COLMAP and self.coords_type == CoordsType.BLENDER):
            R[1, :] *= -1
            R[2, :] *= -1
            T[1] *= -1
            T[2] *= -1
        self.R = R
        self.T = T
        return self
