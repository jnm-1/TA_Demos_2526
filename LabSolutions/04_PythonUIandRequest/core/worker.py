import os
import time
from idlelib.colorizer import prog

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
        for index, url in enumerate(self.urls):
            filename = url.split("/")[-1]
            save_path = os.path.join(self.save_dir, filename)


            if os.path.exists(save_path):
                self.progress_updated.emit(100)
                self.file_finished.emit(index, True)
                continue

            try:
                res =  requests.get(url, stream=True)
                res.raise_for_status()

                total_bytes = int(res.headers.get('content-length', 0))
                downloaded = 0
                print(total_bytes)

                with open(save_path, "wb") as f:
                    for chunk in res.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)

                        if total_bytes > 0:
                            progress = int((downloaded/total_bytes)*100)
                            self.progress_updated.emit(progress)


                self.file_finished.emit(index, True)

            except Exception as e:
                print(f"Failed {url}: {e}")
                self.file_finished.emit(index, False)
