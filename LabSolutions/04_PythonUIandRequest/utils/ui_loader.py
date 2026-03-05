"""
Utility module for loading Qt Designer UI files.
"""
from PySide6.QtUiTools import QUiLoader

def load_ui(ui_filename: str, parent=None):
    """
    Loads a Qt Designer XML file and returns the widget.

    Args:
        ui_filename (str): The relative or absolute path to the .ui file.
        parent (QWidget, optional): The parent widget. Defaults to None.

    Returns:
        QWidget: The fully constructed UI widget from the XML file.
    """
    return QUiLoader().load(ui_filename, parent)