"""
Blender Addon Starter Template
-------------------------------
Based on Blender's built-in "Ui Panel Simple" template.
Use this as your starting point for all Blender addons in PyCharm.

HOW TO USE:
1. Copy this file and rename it for your addon
2. Change the bl_info, class names, and bl_idname values
3. Write your logic inside the execute() method
4. Run in Blender: Scripting workspace → Open → Alt+P
"""

bl_info = {
    "name": "Lab Addon",
    "author": "Jan Mentzel",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "description": "Example of stuff in class",
    "category": "Object",
}

import bpy
import os
from pathlib import Path

# ── Operator ─────────────────────────────────────────────────────────
# This is where your logic goes. One operator = one action / button.

class CLASSDEMO_OT_print_something(bpy.types.Operator):
    """This is just a test print"""
    bl_idname = "class_demo.print_something"
    bl_label = "Do test print!"

    def execute(self, context):
        mesh_count = 0
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                vert_count = len(obj.data.vertices)
                self.report({'INFO'}, f"{obj.name} - {vert_count} verts")
                mesh_count += 1
        if mesh_count == 0:
            self.report({'WARNING'}, "No mesh objects found!")
        return {'FINISHED'}

class CLASSDEMO_OT_export(bpy.types.Operator):
    """export fbx files"""
    bl_idname = "class_demo.export"
    bl_label = "Export current selection"

    def execute(self, context):
        selected = []
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                selected.append(obj)
        if not selected:
            self.report({'WARNING'}, "No mesh selected!")
            return {'CANCELLED'}

        export_dir = os.path.join(Path.home(), "blender_exports")
        os.makedirs(export_dir, exist_ok=True)

        for obj in selected:
            bpy.ops.object.select_all(action ="DESELECT")
            obj.select_set(True)
            context.view_layer.objects.active = obj

            filepath = os.path.join(export_dir, f"{obj.name}.fbx")
            bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)
            self.report({'INFO'}, f"{filepath} exported!")


        return {'FINISHED'}




# ── Panel ────────────────────────────────────────────────────────────
# This creates the sidebar panel in the 3D Viewport (press N to show).

class CLASSDEMO_PT_panel(bpy.types.Panel):
    """Test Panel"""
    bl_label = "Class demo panel"
    bl_idname = "CLASSDEMO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TA Tools"

    def draw(self, context):
        layout = self.layout
        layout.operator("class_demo.print_something")
        layout.separator()
        layout.operator("class_demo.export")


# ── Register / Unregister ────────────────────────────────────────────
# Blender calls these when loading/unloading the addon.
# Same concept as start_plugin() / close_plugin() in Substance Painter.

classes = (
    CLASSDEMO_OT_print_something,
    CLASSDEMO_OT_export,
    CLASSDEMO_PT_panel
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
