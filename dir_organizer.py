#!/usr/bin/python3

import json
import logging
import os
import shutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def load_config(config_file):
    with open(config_file) as f:
        return json.load(f)


class DownloadedFileHandler(FileSystemEventHandler):
    def __init__(self, default_path):
        self.default_path = default_path
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            file_types = load_config(f"{path}/file_types.json")
            created_file = event.src_path
            for key, values in file_types.items():
                if created_file.lower().endswith(tuple(values)):
                    target_dir = os.path.join(self.default_path, key)
                    file_name = os.path.basename(created_file)
                    target_file = os.path.join(target_dir, file_name)
                    try:
                        os.makedirs(target_dir, exist_ok=True)
                        shutil.move(created_file, target_file)
                    except Exception as e:
                        logging.error(f"Error moving file {created_file}: {e}")
                    break


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = os.getenv("USE_PATH")
    watch_path = os.getenv("WATCH_PATH")
    event_handler = DownloadedFileHandler(watch_path)
    observer = Observer()
    observer.schedule(event_handler, watch_path, recursive=True)
    observer.start()
    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
