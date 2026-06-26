from pathlib import Path
from config import SOURCE_DIR, MEDIA_EXTENSIONS


def scan_files():
    files = []

    for p in SOURCE_DIR.rglob("*"):
        if not p.is_file():
            continue

        if p.suffix.lower() not in MEDIA_EXTENSIONS:
            continue

        files.append(p)

    return files