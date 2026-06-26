# metadata.py

from pathlib import Path
from PIL import Image, ExifTags
import pillow_heif
import reverse_geocoder as rg
from datetime import datetime

pillow_heif.register_heif_opener()

GPS_TAGS = ExifTags.GPSTAGS


def get_capture_date(path: Path):
    """
    Returns datetime.
    Falls back to file modified time.
    """
    try:
        img = Image.open(path)
        exif = img.getexif()

        if exif:
            for tag_id, value in exif.items():
                tag = ExifTags.TAGS.get(tag_id)

                if tag in ("DateTimeOriginal", "DateTime"):
                    return datetime.strptime(
                        value,
                        "%Y:%m:%d %H:%M:%S"
                    )
    except:
        pass

    return datetime.fromtimestamp(
        path.stat().st_mtime
    )


def _convert_gps_to_decimal(values):
    d, m, s = values

    def to_float(v):
        try:
            return float(v)
        except:
            return float(v.numerator) / float(v.denominator)

    return (
        to_float(d)
        + to_float(m) / 60
        + to_float(s) / 3600
    )


def get_gps(path: Path):
    """
    Returns:
        lat, lon, city, country
    """

    try:
        img = Image.open(path)
        exif = img.getexif()

        gps_info = None

        for tag_id, value in exif.items():
            tag = ExifTags.TAGS.get(tag_id)

            if tag == "GPSInfo":
                gps_info = value
                break

        if not gps_info:
            return None, None, None, None

        gps = {}

        for k, v in gps_info.items():
            gps[GPS_TAGS.get(k)] = v

        lat = _convert_gps_to_decimal(
            gps["GPSLatitude"]
        )

        lon = _convert_gps_to_decimal(
            gps["GPSLongitude"]
        )

        if gps.get("GPSLatitudeRef") == "S":
            lat *= -1

        if gps.get("GPSLongitudeRef") == "W":
            lon *= -1

        result = rg.search(
            (lat, lon),
            mode=1
        )[0]

        city = result["name"]
        country = result["cc"]

        return lat, lon, city, country

    except:
        return None, None, None, None