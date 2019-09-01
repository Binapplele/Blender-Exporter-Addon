bl_info = {
    "name": "John's Exporter",
    "author": "John Binary",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Object > Export",
    "description": "Export the selected objects to .fbx files (no need to move the objects to world origin) / Support exporting multiple obejcts at the same time",
    "warning": "",
    "wiki_url": "",
    "category": "Export",
}


import bpy
import os
from bpy.types import Operator


def export_selected_objects():
    # the .blend file path
    blend_file_path = bpy.data.filepath 

    # the directory path which .blend file is in
    directory = os.path.dirname(blend_file_path)

    # the Mesh folder for .fbx file
    export_mesh_directory = os.path.join(directory, "Mesh") 
    if not os.path.exists(export_mesh_directory):
        os.makedirs(export_mesh_directory)

    # get selected objects names
    selected_obj_names_list = bpy.context.selected_objects
    for i in selected_obj_names_list:
        selected_object_name = i.name

        # location backup
        bk_location = bpy.data.objects[selected_object_name].location.copy()

        # move obj to world origin
        bpy.data.objects[selected_object_name].location = (0,0,0)

        # export each one individually
        bpy.ops.object.select_all(action='DESELECT')
        i.select_set(state=True)
        target_file = os.path.join(export_mesh_directory, selected_object_name + ".fbx")
        bpy.ops.export_scene.fbx(filepath = target_file, use_selection = True, use_mesh_modifiers = True) 

        # move obj back
        bpy.data.objects[selected_object_name].location = bk_location


class OBJECT_OT_export(Operator):
    bl_label = "Export"
    bl_idname = "object.export"
    bl_desription = "Yeah!"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        export_selected_objects()
        
        return {'FINISHED'}



# Registration

def export_button(self, context):
    self.layout.operator(
        OBJECT_OT_export.bl_idname, text="Export", icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def exporter_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_export)
    bpy.utils.register_manual_map(exporter_manual_map)
    bpy.types.VIEW3D_MT_object.append(export_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_export)
    bpy.utils.unregister_manual_map(exporter_manual_map)
    bpy.types.VIEW3D_MT_object.remove(export_button)


if __name__ == "__main__":
    register()       