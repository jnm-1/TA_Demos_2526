from PySide6.QtUiTools import QUiLoader
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
import substance_painter as sp

import substance_painter.textureset as ts
import substance_painter.layerstack as ls
import substance_painter.resource as res

MATERIALS = ["Iron Forged Old", "Plastic", "Aluminium Brushed Worn"]
MASKS = ["Paint Subtle Scratched", "Stains Surface", "Moss From Top"]



def load_ui(ui_filename: str, parent: QWidget = None) -> QWidget:
    """
    Loads a Qt Designer XML file and returns the widget.
    :param ui_filename:  The relative or absolute path to the .ui file.
    :param parent: The parent widget. Defaults to None.
    :return: The fully constructed UI widget from the XML file.
    """
    return QUiLoader().load(ui_filename, parent)


plugin_widgets = {}
plugin_events = []


def start_plugin():
    """
    Initialize plugin
    """
    # Step 1: Main widget -> Add main layout to this or load from file
    main_widget = QtWidgets.QWidget()

    main_widget.setWindowTitle("Material + Mask")
    # Step 2: Add custom logic here

    layout = QtWidgets.QVBoxLayout()

    mat_combo = QtWidgets.QComboBox()
    mat_combo.addItems(MATERIALS)

    mask_combo = QtWidgets.QComboBox()
    mask_combo.addItems(MASKS)

    button = QtWidgets.QPushButton("Apply Material with Mask")
    status =QtWidgets.QLabel("")

    def apply_material():
        # check project open?
        if not sp.project.is_open():
            status.setText("⚠️ No Project open!")
            return
        # find current selected dropdowns
        mat_name = mat_combo.currentText()
        mask_name = mask_combo.currentText()

        # find and insert material
        mat_results = res.search(f"u:smartmaterial n:{mat_name}")
        if not mat_results:
            status.setText(f"Material {mat_name} not found")
            return

        stack = ts.get_active_stack()
        pos = ls.InsertPosition.from_textureset_stack(stack)
        new_layer = ls.insert_smart_material(pos, mat_results[0].identifier())

        # add a mask slot
        new_layer.add_mask(ls.MaskBackground.White)

        # find and insert smart mask
        mask_results = res.search(f"u:smartmask n:{mask_name}")
        if not mask_results:
            status.setText(f"Material created but mask {mask_name} not found")
            return
        mask_pos = ls.InsertPosition.inside_node(new_layer, ls.NodeStack.Mask)
        ls.insert_smart_mask(mask_pos, mask_results[0].identifier())
        status.setText("Applied mask and material")

    button.clicked.connect(apply_material)
    layout.addWidget(mat_combo)
    layout.addWidget(mask_combo)
    layout.addWidget(button)
    layout.addWidget(status)
    main_widget.setLayout(layout)

    # Step 3: Adding to painter (DONT TOUCH)
    docked_widget = sp.ui.add_dock_widget(main_widget)
    plugin_widgets[docked_widget] = main_widget


def close_plugin():
    """
    Close plugin
    """

    # Step 2: Cleanup widgets (DONT TOUCH)
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
