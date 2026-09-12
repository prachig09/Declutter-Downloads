import time
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from src.config import WATCH_DIR, DRY_RUN
from src.file_handler import process_file

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

if __name__ == "__main__":
    print(f"File Sorter Active! Watching: {WATCH_DIR} (Dry Run: {DRY_RUN})")
    
    event_handler = DownloadHandler()
    observer = PollingObserver(timeout=1.0)
    observer.schedule(event_handler, path=WATCH_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()