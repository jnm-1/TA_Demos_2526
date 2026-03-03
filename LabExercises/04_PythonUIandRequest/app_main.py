import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QAbstractItemView
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt

from utils.ui_loader import load_ui
from core import config_manager
from core.worker import DownloadWorker
from bonus_inspector import LidarInspector

class LidarDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # We load the UI as a Widget and set it as the Central Widget
        # TODO: make sure to use your QT file instead
        self.ui = load_ui("resources/main_window_backup.ui", self)
        self.setCentralWidget(self.ui)
        self.setWindowTitle("LiDAR Downloader")

        # TODO: Enable extended selection for the list widget

        # TODO: Connect UI signals (button clicks, text changes) to our slots

        # TODO: Load saved path from config_manager

    def validate_inputs(self):
        """
        Checks if the save path is a valid directory and if there are links.
        Enables or disables the download button accordingly.
        """
        pass

    def browse_folder(self):
        """
        Opens a QFileDialog to select a save directory.
        Saves the chosen path to config.
        """
        pass

    def add_local_files(self):
        """
        Opens a QFileDialog to manually add local .laz/.las files to the list.
        """
        pass

    def start_download(self):
        """
        Parses the URLs from the text box, populates the UI list,
        and starts the DownloadWorker thread.
        """
        pass

    def handle_finished(self, index: int, success: bool):
        """
        Updates the UI list when a file finishes downloading.
        Secretly embeds the absolute file path into the list item using Qt.UserRole.
        """
        pass

    def open_inspector(self):
        """
        Extracts the hidden file paths from selected list items
        and launches the 2D LiDAR viewer.
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LidarDownloaderApp()
    window.show()
    sys.exit(app.exec())