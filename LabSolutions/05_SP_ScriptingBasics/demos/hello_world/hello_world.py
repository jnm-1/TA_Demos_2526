from PySide6 import QtWidgets
import substance_painter as sp


plugin_widgets = []

def start_plugin():


    button = QtWidgets.QPushButton("Say Hello!")
    button.clicked.connect(lambda: sp.logging.info("Hello World"))
    button.setWindowTitle("test title")
    dock_widget = sp.ui.add_dock_widget(button)
    plugin_widgets.append(button)
    plugin_widgets.append(dock_widget)


def close_plugin():
    for dock_widget in plugin_widgets:
        sp.ui.delete_ui_element(dock_widget)

    plugin_widgets.clear()