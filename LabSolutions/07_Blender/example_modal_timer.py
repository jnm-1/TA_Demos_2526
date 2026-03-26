"""
SHOWCASE: Modal Timer + Subprocess
Demonstrates launching an external process without freezing Blender's UI.

HOW TO USE IN CLASS:
- This is NOT a code-along — run it on screen, students watch
- Show the dummy_slow_task.py script first so they know what it does
- Run this addon, click the button, show Blender stays responsive
- After 3 seconds the status updates — "same concept as QThread from Week 4"

IMPORTANT: Update DUMMY_SCRIPT_PATH below to point at dummy_slow_task.py!
"""

bl_info = {
    "name": "Modal Timer Showcase",
    "author": "TA Class",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "description": "Runs an external process without freezing Blender",
    "category": "Object",
}

import os
import sys
import subprocess
import bpy


# ── UPDATE THIS PATH to where dummy_slow_task.py lives ───────────────
# Hardcoded so it works when running from Blender's text editor (Alt+P).
# __file__ is not set when running from the text editor.
DUMMY_SCRIPT_PATH = r"/LabSolutions/07_Blender/dummy_slow_task.py"
RESULT_FILE_PATH = os.path.join(os.path.expanduser("~"), "blender_exports", "task_result.txt")


class MODAL_OT_run_task(bpy.types.Operator):
    """Launch an external task and wait for it without freezing Blender"""
    bl_idname = "modal_demo.run_task"
    bl_label = "Run External Task"

    _timer = None
    _process = None

    def execute(self, context):
        # Make sure the output dir exists
        os.makedirs(os.path.dirname(RESULT_FILE_PATH), exist_ok=True)

        # Remove old result file if it exists
        if os.path.isfile(RESULT_FILE_PATH):
            os.remove(RESULT_FILE_PATH)

        # Launch the dummy script as a subprocess (non-blocking!)
        self._process = subprocess.Popen(
            [sys.executable, DUMMY_SCRIPT_PATH, RESULT_FILE_PATH],
        )

        # Add a timer that fires every 0.5 seconds
        self._timer = context.window_manager.event_timer_add(0.5, window=context.window)
        context.window_manager.modal_handler_add(self)

        self.report({'INFO'}, "Task started... Blender is NOT frozen!")
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'TIMER':
            # Check if the subprocess has finished
            if self._process.poll() is not None:
                # Process done — clean up the timer
                context.window_manager.event_timer_remove(self._timer)

                # Check if the result file was written
                if os.path.isfile(RESULT_FILE_PATH):
                    with open(RESULT_FILE_PATH, "r") as f:
                        result = f.read().strip()
                    self.report({'INFO'}, f"Task finished! Result: {result}")
                else:
                    self.report({'WARNING'}, "Task finished but no result file found")

                return {'FINISHED'}

        return {'PASS_THROUGH'}  # Don't block Blender's other events

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._process:
            self._process.kill()


class MODAL_PT_panel(bpy.types.Panel):
    """Modal Timer Demo panel"""
    bl_label = "Modal Timer Demo"
    bl_idname = "MODAL_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "TA Tools"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Launches a 3-second task")
        layout.label(text="Blender stays responsive!")
        layout.operator("modal_demo.run_task")


classes = (
    MODAL_OT_run_task,
    MODAL_PT_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
