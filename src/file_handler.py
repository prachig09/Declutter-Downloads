import os
import shutil
import time
from src.config import TAG_RULES, DRY_RUN

TEMP_EXTENSIONS = [".crdownload", ".tmp", ".part", ".download"]

def is_temp_file(filename: str) -> bool:
    return any(filename.lower().endswith(ext) for ext in TEMP_EXTENSIONS) or filename.startswith(".")

def process_file(file_path: str):
    filename = os.path.basename(file_path)

    if is_temp_file(filename) or os.path.isdir(file_path):
        return

    # Give browser write-lock a brief pause to release
    time.sleep(0.5)

    # Tag Matching Engine
    for tag, destination_folder in TAG_RULES.items():
        if tag in filename:
            destination_path = os.path.join(destination_folder, filename)
            move_file(file_path, destination_path)
            return

def move_file(src: str, dst: str):
    if DRY_RUN:
        print(f"[DRY-RUN] Would move: {src} -> {dst}")
        return

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.move(src, dst)
    print(f"[MOVED] {src} -> {dst}")