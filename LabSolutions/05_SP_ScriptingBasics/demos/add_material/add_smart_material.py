from PySide6 import QtWidgets
import substance_painter as sp

plugin_widgets = []


def start_plugin():
    """
    Initialize plugin    
    """
    # sp.ui.add_dock_widget()


def close_plugin():
    """
    Close plugin
    """
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
