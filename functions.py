import bpy
import numpy as np
from .read_write_model import read_model, write_model, qvec2rotmat
from .enums import CoordsType, TransformType
from .camera import Camera
from .utility import add_obj


# import camera
def _add_camera_data(camera, camera_name):
    bcamera = bpy.data.cameras.new(camera_name)
    bcamera.lens = camera.fx
    bcamera.sensor_width = camera.width * camera.fx / camera.cx
    bcamera.sensor_height = camera.height * camera.fy / camera.cy
    bcamera.sensor_fit = 'HORIZONTAL'  # Assuming horizontal sensor fit
    return bcamera

def add_camera_object(
    camera,
    camera_name,
    data,
    camera_collection,
):
    """Add a camera as Blender object."""
    camera = camera.astype(CoordsType.BLENDER).to(TransformType.C2W)
    bcamera = _add_camera_data(camera, camera_name)
    camera_object = add_obj(bcamera, camera_name, camera_collection)
    # custom props
    image_data, camera_data = data
    camera_object['image_data'] = image_data
    camera_object['camera_data'] = camera_data

    camera_object.matrix_world = camera.M.T
    return camera_object

def read_colmap_model(cameras, images):
    # camera
    parent_collection = bpy.context.collection
    new_collection = bpy.data.collections.new('Reconstruction')
    parent_collection.children.link(new_collection)

    for image_id, image in images.items():
        qvec = image.qvec
        tvec = image.tvec
        camera = cameras[image.camera_id]
        new_cam = Camera(
            width=camera.width,
            height=camera.height,
            image_path=image.name,
            R=qvec2rotmat(qvec),
            T=tvec,
            params=camera.params,
            camera_type=camera.model,
            transform_type=TransformType.W2C,
            coords_type=CoordsType.COLMAP
        )
        data = (image._asdict(), camera._asdict())
        add_camera_object(new_cam, image.name, data, new_collection)

def write_colmap_model(cameras, images, mode="selected"):
    """
    Export COLMAP model based on the selected mode.
    
    - 'selected': Use the selected cameras and images in Blender
    - 'original': Use the original COLMAP cameras and images, filtering based on selected camera/image IDs
    """
    selected_cameras = [obj for obj in bpy.context.selected_objects if obj.type == "CAMERA"]
    
    if mode == "selected":
        selected_camera_ids = []
        selected_image_ids = []

        # Gather the selected camera IDs based on their names (which correspond to the camera IDs in COLMAP)
        for cam in selected_cameras:
            camera_id = int(cam.name.split("_")[-1])  # Assuming camera names include their ID (e.g. Camera_1)
            selected_camera_ids.append(camera_id)

        # Filter the images and cameras from COLMAP based on the selected camera IDs
        selected_images = {img_id: img for img_id, img in images.items() if img.camera_id in selected_camera_ids}
        selected_cameras = {cam_id: cam for cam_id, cam in cameras.items() if cam_id in selected_camera_ids}

        # Create the COLMAP model with selected cameras and images
        write_model(selected_cameras, selected_images, points3D={}, path='/home/zhewenz/tmp/', ext=".bin")

    elif mode == "original":
        # When using 'original', find the corresponding cameras and images based on Blender camera IDs
        cameras_to_export = {}
        images_to_export = {}

        for obj in selected_cameras:
            camera_id = int(obj.name.split("_")[-1])
            camera = cameras[camera_id]

            # Get the camera's intrinsic parameters from Blender's data
            R = obj.matrix_world.to_3x3()
            T = obj.matrix_world.to_translation()

            # Create the Camera object with the user-defined data
            user_defined_camera = Camera(
                width=obj.data.sensor_width * 1920 / obj.data.lens,  # Width and height adjustment
                height=obj.data.sensor_height * 1080 / obj.data.lens,  # Based on FOV and sensor size
                image_path=obj.name,
                R=R,
                T=T,
                params=np.array([obj.data.lens, 960, 540]),  # Assume the principal point at (cx, cy)
                camera_type='USER_DEFINED',
                transform_type=TransformType.W2C,
                coords_type=CoordsType.BLENDER
            )

            cameras_to_export[camera_id] = user_defined_camera

            # Create the image object with user-defined extrinsics (matrix_world)
            image_id = camera_id  # Assuming image_id matches camera_id for this export
            images_to_export[image_id] = {
                'id': image_id,
                'camera_id': camera_id,
                'name': obj.name,
                'qvec': np.array([1, 0, 0, 0]),  # Assume identity quaternion
                'tvec': T,  # Use the camera location in Blender
                'xys': np.array([]),  # Empty for now, can be populated if needed
                'point3D_ids': np.array([]),  # Empty for now, can be populated if needed
            }

        # Write the user-defined camera and image data to the COLMAP files
        write_model(cameras_to_export, images_to_export, points3D={}, path='/home/zhewenz/tmp/', ext=".bin")
# load_cameras('/home/zhewenz/research/datasets/mipnerf360/bicycle/sparse/0')