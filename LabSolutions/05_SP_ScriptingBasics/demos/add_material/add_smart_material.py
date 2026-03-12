from PySide6 import QtWidgets
import substance_painter as sp
import substance_painter.textureset as ts
import substance_painter.layerstack as ls
import substance_painter.resource as res



plugin_widgets = []


def start_plugin():
    """
    Initialize plugin    
    """

    widget = QtWidgets.QWidget()
    widget.setWindowTitle("Quick Smart Material")
    layout = QtWidgets.QVBoxLayout()

    input_field = QtWidgets.QLineEdit()
    input_field.setPlaceholderText(" Smart material name (e.g. Iron Forged Old")
    button = QtWidgets.QPushButton("Add to stack")
    status = QtWidgets.QLabel("")

    def add_material():
        """
        find material based on partial name and add to current stack
        :return:
        """
        # is anything entered
        name = input_field.text().strip()
        if not name:
            status.setText("Enter something!")
            return

        # is there a project open
        if not sp.project.is_open():
            status.setText("No project is open!")
            return

        # is there at least 1 valid choice:
        results = res.search(f"u:smartmaterial n:{name}")
        sp.logging.info(f"{str([r.gui_name() for r in results])}")

        if not results:
            status.setText(f"{name} was not found in smart material shelf")
            return

        stack = ts.get_active_stack()
        pos = ls.InsertPosition.from_textureset_stack(stack)
        ls.insert_smart_material(pos, results[0].identifier())
        status.setText(f"Added {results[0].gui_name()} to layer stack!")


    button.clicked.connect(add_material)
    layout.addWidget(input_field)
    layout.addWidget(button)
    layout.addWidget(status)
    widget.setLayout(layout)
    dock_widget = sp.ui.add_dock_widget(widget)
    plugin_widgets.append(widget)
    plugin_widgets.append(dock_widget)


def close_plugin():
    """
    Close plugin
    """
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
