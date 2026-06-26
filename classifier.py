from pathlib import Path


def classify(path: Path):
    name = path.name.lower()
    full = str(path).lower()

    # screenshots
    if "screenshot" in name:
        return "screenshots"

    # whatsapp
    if "whatsapp" in full:
        return "whatsapp"

    if name.startswith("img-"):
        return "whatsapp"

    if name.startswith("vid-"):
        return "whatsapp"

    return "photos"