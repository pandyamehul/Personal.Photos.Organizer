# logger.py

import csv
from config import LOG_DIR

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


def write_duplicate(
        duplicate,
        original,
        sha):

    f = LOG_DIR / "duplicates.csv"

    exists = f.exists()

    with open(
            f,
            "a",
            newline="",
            encoding="utf8") as fp:

        writer = csv.writer(fp)

        if not exists:
            writer.writerow([
                "duplicate",
                "original",
                "sha256"
            ])

        writer.writerow([
            duplicate,
            original,
            sha
        ])


def write_move(
        source,
        destination):

    f = LOG_DIR / "moves.csv"

    exists = f.exists()

    with open(
            f,
            "a",
            newline="",
            encoding="utf8") as fp:

        writer = csv.writer(fp)

        if not exists:
            writer.writerow([
                "source",
                "destination"
            ])

        writer.writerow([
            source,
            destination
        ])


def write_failure(
        file,
        error):

    f = LOG_DIR / "failures.csv"

    exists = f.exists()

    with open(
            f,
            "a",
            newline="",
            encoding="utf8") as fp:

        writer = csv.writer(fp)

        if not exists:
            writer.writerow([
                "file",
                "error"
            ])

        writer.writerow([
            file,
            error
        ])