import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers.polling import PollingObserver

from src.config import DRY_RUN, WATCH_DIR
from src.file_handler import process_file
from src.metrics import start_metrics_server


class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

if __name__ == "__main__":
    # Launch Prometheus HTTP Metrics Server on localhost:8000
    start_metrics_server(8000)

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