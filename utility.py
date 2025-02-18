import bpy


def add_obj(data, obj_name, collection=None):
    """Add an object to the scene."""
    if collection is None:
        collection = bpy.context.collection

    new_obj = bpy.data.objects.new(obj_name, data)
    collection.objects.link(new_obj)
    new_obj.select_set(state=True)

    if (
        bpy.context.view_layer.objects.active is None
        or bpy.context.view_layer.objects.active.mode == "OBJECT"
    ):
        bpy.context.view_layer.objects.active = new_obj
    return new_obj


def parse_camera_model(model: str, params: list) -> tuple:
    f, fx, fy, cx, cy, k, k1, k2, p1, p2, k3, k4, k5, k6 = [None] * 14
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
    return (fx, fy, cx, cy, k1, k2, k3, k4, k5, k6, p1, p2)