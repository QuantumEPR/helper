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