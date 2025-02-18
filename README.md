# Blender COLMAP Model Import/Export Addon

This addon allows you to import and export COLMAP models in Blender. You can easily load COLMAP camera and image data into Blender and export selected objects back into COLMAP format.

## Installation

1. Download the ZIP file of this repository.
2. Open Blender.
3. Go to `Edit > Preferences > Add-ons`.
4. In the top-right dropdown, click on `Install from Disk`.
5. Select the ZIP file you downloaded.
6. Make sure the addon is enabled by checking the checkbox next to it in the Add-ons list.

**Note:** If you encounter errors related to imports, ensure that Blender's Python (located in the directory where Blender is installed) has `numpy` installed.

## Usage

### Import COLMAP Model
To import a COLMAP model (cameras and images):

1. Go to `File > Import > COLMAP Model (.bin)`.
2. Choose your `.bin` file that contains the COLMAP model data.
3. The cameras and images will be imported into the Blender scene.

### Export COLMAP Model
To export a COLMAP model (only selected objects):

1. Select the objects you want to export in the 3D viewport.
2. Go to `File > Export > COLMAP Model (.bin)`.
3. Choose the destination to save the `.bin` file containing the selected objects.

## Requirements

- Blender (tested on 4.3)
- Python `numpy` module (ensure it's installed in Blender’s Python environment)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
