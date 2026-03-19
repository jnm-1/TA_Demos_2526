from PySide6.QtUiTools import QUiLoader
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget
import substance_painter as sp
import substance_painter.baking as baking
import substance_painter.event as event
import substance_painter.textureset as ts


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

    main_widget.setWindowTitle("One click Bake")
    # Step 2: Add custom logic here

    layout = QtWidgets.QVBoxLayout()
    button = QtWidgets.QPushButton("🔥 Bake all Maps")
    status = QtWidgets.QLabel("Ready")

    def on_bake_finished(e):
        status.setText(f"✅ Bake finished! ({e.status})")
        button.setEnabled(True)

    # connect the callback (its like signal or event dispatcher in unreal)
    event.DISPATCHER.connect_strong(event.BakingProcessEnded, on_bake_finished)
    plugin_events.append((event.BakingProcessEnded, on_bake_finished ))

    def run_bake():
        if not sp.project.is_open():
            status.setText("⚠️ No Project open!")
            return
        status.setText("Baking...")
        button.setEnabled(False)

        all_sets = ts.all_texture_sets()
        if all_sets:
            baking.bake_async(all_sets[0])

    button.clicked.connect(run_bake)
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
    # Step 1: Add custom logic
    for evt, cb in plugin_events:
        event.DISPATCHER.disconnect(evt, cb)
    plugin_events.clear()


    # Step 2: Cleanup widgets (DONT TOUCH)
    for widget in plugin_widgets:
        sp.ui.delete_ui_element(widget)

    plugin_widgets.clear()
