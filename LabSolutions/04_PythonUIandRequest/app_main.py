import sys
import os
from fileinput import filename

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
        self.btn_add_local: QPushButton = self.ui.btn_add_local
        self.btn_inspect: QPushButton = self.ui.btn_inspect
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

        # Load saved path from config_manager

        config = config_manager.load_config()
        saved_path = config.get("last_save_path", "")
        if saved_path and os.path.isdir(saved_path):
            self.line_path.setText(saved_path)

    def validate_inputs(self):
        """
        Checks if the save path is a valid directory and if there are links.
        Enables or disables the download button accordingly.
        """
        valid_dir = os.path.isdir(self.line_path.text().strip())
        has_links = len(self.text_links.toPlainText().strip()) > 0
        self.btn_download.setEnabled(valid_dir and has_links)

    def browse_folder(self):
        """
        Opens a QFileDialog to select a save directory.
        Saves the chosen path to config.
        """
        folder = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        #this is a folder picker
        if folder:
            self.line_path.setText(folder)
            config_manager.save_config({"last_save_path": folder})

    def add_local_files(self):
        """
        Opens a QFileDialog to manually add local .laz/.las files to the list.
        """
        # this is a file picker
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select Local Lidar Files", "", "Lidar files (*.laz *.las)")

        for path in file_paths:
            filename = os.path.basename(path)
            # use Windows key and . to find emojies
            item = QListWidgetItem(f"✅ {filename}")
            item.setForeground(QColor("green"))
            item.setData(Qt.UserRole, path)
            self.list_tasks.addItem(item)

    def start_download(self):
        raw_text = self.ui.text_links.toPlainText()
        urls = [line.strip() for line in raw_text.split("\n") if line.strip()]
        save_dir = self.ui.line_path.text().strip()

        if not urls or not save_dir:
            return

        self.ui.list_tasks.clear()

        # Populate list and temporarily store standard filenames
        for u in urls:
            filename = u.split("/")[-1]
            item = QListWidgetItem(filename)
            self.ui.list_tasks.addItem(item)

        self.ui.btn_download.setEnabled(False)
        self.ui.progress_current.setValue(0)

        self.worker = DownloadWorker(urls, save_dir)
        self.worker.progress_updated.connect(self.ui.progress_current.setValue)
        self.worker.file_finished.connect(self.handle_finished)
        self.worker.start()

    def handle_finished(self, index: int, success: bool):
        """Updates the queue visually and embeds the absolute path secretly."""
        item = self.ui.list_tasks.item(index)
        if success:
            item.setText(f"✅ {item.text()}")
            item.setForeground(QColor("green"))

            # TEACHING MOMENT: Store the absolute path securely inside the item!
            save_dir = self.ui.line_path.text().strip()
            filename = item.text().replace("✅ ", "")
            full_path = os.path.join(save_dir, filename)
            item.setData(Qt.UserRole, full_path)
        else:
            item.setText(f"❌ {item.text()}")
            item.setForeground(QColor("red"))

        if index == self.ui.list_tasks.count() - 1:
            self.validate_inputs()

    def open_inspector(self):
        """Extracts the hidden file paths and launches the 2D viewer."""
        selected = self.ui.list_tasks.selectedItems()
        if not selected:
            return

        valid_file_paths = []
        for item in selected:
            # Safely grab the absolute path we hid earlier
            file_path = item.data(Qt.UserRole)
            if file_path and os.path.exists(file_path):
                valid_file_paths.append(file_path)

        if not valid_file_paths:
            return

        self.inspector = LidarInspector(valid_file_paths)
        self.inspector.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LidarDownloaderApp()
    window.show()
    sys.exit(app.exec())


