# mover.py

import shutil
from pathlib import Path
from config import DRY_RUN


def ensure_folder(folder):
    folder.mkdir(
        parents=True,
        exist_ok=True
    )


def unique_target(
    folder,
    filename
):
    target = folder / filename

    i = 1

    while target.exists():
        target = (
            folder
            / f"{target.stem}_{i}"
              f"{target.suffix}"
        )
        i += 1

    return target


def move_file(
    source,
    destination_folder
):
    ensure_folder(
        destination_folder
    )

    target = unique_target(
        destination_folder,
        source.name
    )

    if not DRY_RUN:
        shutil.move(
            str(source),
            str(target)
        )

    return target