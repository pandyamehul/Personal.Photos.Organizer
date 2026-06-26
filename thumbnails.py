# thumbnails.py

from pathlib import Path
from PIL import Image
from config import THUMB_DIR
from config import THUMB_SIZE


def create_thumbnail(
        source):

    THUMB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    safe_name = (
        str(source)
        .replace(":", "_")
        .replace("\\", "_")
        .replace("/", "_")
    )

    thumb = (
        THUMB_DIR
        / f"{safe_name}.jpg"
    )

    if thumb.exists():
        return thumb

    try:
        img = Image.open(source)

        img.thumbnail(
            THUMB_SIZE
        )

        img = img.convert("RGB")

        img.save(
            thumb,
            "JPEG",
            quality=75
        )

        return thumb

    except:
        return None