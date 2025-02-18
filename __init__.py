bl_info = {
    "name": "COLMAP Model Import/Export",
    "blender": (2, 82, 0),
    "category": "Import-Export",
}

import bpy
import os
from .functions import read_colmap_model, write_colmap_model
from .read_write_model import read_model, write_model

# Import Operator to handle file selection for COLMAP models
class ImportCOLMAPModelOperator(bpy.types.Operator):
    bl_idname = "import_scene.colmap_model"
    bl_label = "Import COLMAP Model"
    
    # Path of the folder selected by the user
    filepath: bpy.props.StringProperty(subtype="DIR_PATH") # type: ignore

    def execute(self, context):
        if os.path.isdir(self.filepath):
            read_colmap_model(self.filepath)
            self.report({"INFO"}, f"Imported cameras from {self.filepath}")
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid folder path")
            return {"CANCELLED"}

    def invoke(self, context, event):
        # Open file browser to select the folder containing .bin files
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}


class ExportCOLMAPModelOperator(bpy.types.Operator):
    bl_idname = "export_scene.colmap_model"
    bl_label = "Export COLMAP Model"

    filepath: bpy.props.StringProperty(subtype="DIR_PATH") # type: ignore
    export_mode: bpy.props.EnumProperty(
        items=[("selected", "Selected Cameras and Images", ""),
               ("original", "User-defined Cameras and Images", "")],
        name="Export Mode",
        default="selected"
    ) # type: ignore

    def execute(self, context):
        if os.path.isdir(self.filepath):
            write_colmap_model(self.filepath)
            self.report({"INFO"}, f"Exported COLMAP model to {self.filepath} using mode {self.export_mode}")
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, "Invalid folder path")
            return {"CANCELLED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}




# Panel to show the import and export options
class COLMAPPanel(bpy.types.Panel):
    bl_label = "COLMAP Model Import/Export"
    bl_idname = "OBJECT_PT_colmap_model"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "COLMAP"

    def draw(self, context):
        layout = self.layout
        layout.operator("import_scene.colmap_model", text="Import COLMAP Model")
        layout.operator("export_scene.colmap_model", text="Export COLMAP Model")


# Register and Unregister functions to handle the addon lifecycle
def menu_func_import(self, context):
    self.layout.operator("import_scene.colmap_model", text="COLMAP Model (.bin)")


def menu_func_export(self, context):
    self.layout.operator("export_scene.colmap_model", text="COLMAP Model (.bin)")



def register():
    bpy.utils.register_class(ImportCOLMAPModelOperator)
    bpy.utils.register_class(ExportCOLMAPModelOperator)
    bpy.utils.register_class(COLMAPPanel)
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    print("Registered 3 modules.")

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.utils.unregister_class(COLMAPPanel)
    bpy.utils.unregister_class(ExportCOLMAPModelOperator)
    bpy.utils.unregister_class(ImportCOLMAPModelOperator)
    print("Unegistered 3 modules.")


if __name__ == "__main__":
    print("INFO", "main called")