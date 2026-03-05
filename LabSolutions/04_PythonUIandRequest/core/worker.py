import os
import time
import requests
from PySide6.QtCore import QThread, Signal

class DownloadWorker(QThread):
    """
    Background thread for downloading URLs sequentially.
    Skips files that already exist on disk to save bandwidth.
    """
    progress_updated = Signal(int)
    eta_updated = Signal(str)
    file_finished = Signal(int, bool)

    # we inherit from QThread and then overwrite the run function. Because we also make our own init we need to call
    # the init of the parent class using super to run the original init as well.
    def __init__(self, urls: list, save_dir: str):
        super().__init__()
        self.urls = urls
        self.save_dir = save_dir

    def run(self):
        """
        Main loop that processes the download queue.
        Emits progress, ETA, and completion signals.
        """
        pass