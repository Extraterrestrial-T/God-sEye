import os
import cv2
from datetime import datetime

# Ensure directories exist
BASE_DIR = os.getcwd()
SNAPSHOT_DIR = os.path.join(BASE_DIR, 'assets', 'snapshots')
LOG_FILE = os.path.join(BASE_DIR, 'logs', 'events.log')
os.makedirs(SNAPSHOT_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def save_frame(frame, suffix=''):
    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')
    fname = f'frame_{ts}{suffix}.jpg'
    path = os.path.join(SNAPSHOT_DIR, fname)
    cv2.imwrite(path, frame)
    log_event(f"Saved frame: {fname}")
    return path


def log_event(message: str):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    entry = f"[{ts}] {message}\n"
    with open(LOG_FILE, 'a') as f:
        f.write(entry)