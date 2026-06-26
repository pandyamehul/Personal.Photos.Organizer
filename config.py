from pathlib import Path

# CHANGE THESE
SOURCE_DIR = Path(r"D:\iPhoneBackup")
DEST_DIR = Path(r"E:\OrganizedPhotos")

DB_PATH = DEST_DIR / "photos.db"
THUMB_DIR = DEST_DIR / "thumbnails"

DRY_RUN = True

# event detection
EVENT_MIN_PHOTOS = 50
EVENT_MAX_GAP_HOURS = 6

# thumbnail size
THUMB_SIZE = (400, 400)

PHOTO_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".heic",
    ".png"
}

VIDEO_EXTENSIONS = {
    ".mov",
    ".mp4",
    ".m4v"
}

MEDIA_EXTENSIONS = PHOTO_EXTENSIONS | VIDEO_EXTENSIONS

LOG_DIR = DEST_DIR / "logs"