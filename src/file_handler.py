import os
import shutil
import time

from src import config
from src.metrics import (
    FILE_PROCESSING_SECONDS,
    FILES_SORTED_TOTAL,
    UNMATCHED_FILES_TOTAL,
)

TEMP_EXTENSIONS = [".crdownload", ".tmp", ".part", ".download"]

def is_temp_file(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in TEMP_EXTENSIONS) or filename.startswith(".")

def process_file(file_path: str):
    filename = os.path.basename(file_path)

    if is_temp_file(filename) or os.path.isdir(file_path):
        return

    start_time = time.time()
    matched = False

    time.sleep(0.5)

    # Access config.TAG_RULES dynamically
    for tag, destination_folder in config.TAG_RULES.items():
        if tag in filename:
            matched = True
            category_name = tag.strip("_")
            destination_path = os.path.join(destination_folder, filename)
            move_file(file_path, destination_path, category_name)
            break

    if not matched:
        UNMATCHED_FILES_TOTAL.inc()

    duration = time.time() - start_time
    FILE_PROCESSING_SECONDS.observe(duration)

def move_file(src: str, dst: str, category: str):
    if config.DRY_RUN:
        print(f"[DRY-RUN] Would move: {src} -> {dst}")
        FILES_SORTED_TOTAL.labels(category=category, status="success").inc()
        return

    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.move(src, dst)
        print(f"[MOVED] {src} -> {dst}")
        FILES_SORTED_TOTAL.labels(category=category, status="success").inc()
    except OSError as e:
        print(f"[ERROR] Failed to move {src}: {e}")
        FILES_SORTED_TOTAL.labels(category=category, status="failed").inc()