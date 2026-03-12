from PySide6 import QtWidgets
import substance_painter as sp
import substance_painter.textureset as ts

plugin_widgets = []


def start_plugin():
    """
    Initialize plugin    
    """

    widget =  QtWidgets.QWidget()
    widget.setWindowTitle("Texture set info")
    layout = QtWidgets.QVBoxLayout()
    button = QtWidgets.QPushButton("Fetch Info")
    output = QtWidgets.QTextEdit()
    output.setReadOnly(True)

    def list_texture_sets():
        output.clear()

        if not sp.project.is_open():
            output.setText("No project is open!!!!!")
            return

        for texture_set in ts.all_texture_sets():
            name = texture_set.name
            resolution = texture_set.get_resolution()
            output.append(f"{name} - {resolution.width} x {resolution.height}")

    button.clicked.connect(list_texture_sets)

    layout.addWidget(button)
    layout.addWidget(output)
    widget.setLayout(layout)
    docked_widget = sp.ui.add_dock_widget(widget)

    plugin_widgets.append(docked_widget)
    plugin_widgets.append(widget)




def close_plugin():
    """
    Close plugin
    """
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
