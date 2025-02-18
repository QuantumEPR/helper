import bpy
import numpy as np
from dataclasses import asdict
from .read_write_model import (
    read_model, 
    write_model, 
    qvec2rotmat, 
    Image as ColmapImage,
    Camera as ColmapCamera
)
from .utility import add_obj


# import camera
def _add_camera_data(camera, camera_name):
    intr, extr = camera
    bcamera = bpy.data.cameras.new(camera_name)
    bcamera.lens = intr.fx
    bcamera.sensor_width = intr.width * intr.fx / intr.cx
    bcamera.sensor_height = intr.height * intr.fy / intr.cy
    bcamera.sensor_fit = 'HORIZONTAL'  # Assuming horizontal sensor fit
    return bcamera

def add_camera_object(
    camera: tuple,
    camera_name,
    camera_collection,
):
    """Add a camera as Blender object."""
    intr, extr = camera
    bcamera = _add_camera_data(camera, camera_name)
    camera_object = add_obj(bcamera, camera_name, camera_collection)
    
    # set camera with corresponding pose
    camera_object.matrix_world = np.linalg.inv(np.array(extr.matrix)).T # converts to C2W and then uses column major.
    
    # assign custom props for deserialization
    camera_object['camera'] = intr._asdict()
    camera_object['image'] = extr._asdict()

    return camera_object

def read_colmap_model(filepath):
    intrinsics, extrinsics, _ = read_model(filepath, ext='.bin')
    # setup new collection
    parent_collection = bpy.context.collection
    new_collection = bpy.data.collections.new('Reconstruction')
    parent_collection.children.link(new_collection)

    for eid, extr in extrinsics.items():
        extr = extrinsics[eid]
        iid = extr.camera_id
        intr = intrinsics[iid]
        camera = (intr, extr)
        add_camera_object(camera, extr.name, new_collection)

def write_colmap_model(filepath):
    """
    Export COLMAP model based on the selected mode.
    
    - 'selected': Use the selected cameras and images in Blender
    - 'original': Use the original COLMAP cameras and images, filtering based on selected camera/image IDs
    """
    selected_bcameras = [obj for obj in bpy.context.selected_objects if obj.type == "CAMERA"]
    
    intrinsics = {}
    extrinsics = {}

    for camera_object in selected_bcameras:
        # assemble back into colmap format
        extr = camera_object['image']
        intr = camera_object['camera']
        iid = extr['camera_id']
        eid = extr['id']
        intrinsics[iid] = ColmapCamera(**intr)
        extrinsics[eid] = ColmapImage(**extr)

    # Create the COLMAP model with selected cameras and images
    write_model(intrinsics, extrinsics, points3D={}, path=filepath, ext=".bin")