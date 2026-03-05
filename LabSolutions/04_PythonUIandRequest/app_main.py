import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QAbstractItemView, QPushButton, \
    QLineEdit, QPlainTextEdit, QListWidget

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
        self.ui = load_ui("resources/main_window.ui", self)
        self.setCentralWidget(self.ui)
        self.setWindowTitle("LiDAR Downloader")

        # make variables with correct type for UI Elements so intellisense works as expected
        self.btn_browse: QPushButton = self.ui.btn_browse
        self.btn_download: QPushButton = self.ui.btn_download
        self.btn_add_local: QPushButton = self.ui.add_local
        self.btn_inspect: QPushButton = self.ui.inspect
        self.line_path: QLineEdit = self.ui.line_path
        self.text_links: QPlainTextEdit = self.ui.text_links
        self.list_tasks: QListWidget = self.ui.list_tasks


        # Enable extended selection for the list widget
        self.list_tasks.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # TODO: Connect UI signals (button clicks, text changes) to our slots

        self.btn_browse.clicked.connect(self.browse_folder)
        self.btn_download.clicked.connect(self.start_download)
        self.btn_add_local.clicked.connect(self.add_local_files)
        self.btn_inspect.clicked.connect(self.open_inspector)

        self.line_path.textChanged.connect(self.validate_inputs)
        self.text_links.textChanged.connect(self.validate_inputs)

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