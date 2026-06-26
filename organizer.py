# organizer.py

from pathlib import Path
from tqdm import tqdm

from config import *
from database import *
from scanner import scan_files
from duplicates import *
from metadata import *
from classifier import *
from events import *
from mover import *
from thumbnails import *
from livephotos import *

from logger import *


def index_files(
        conn,
        files):

    print(
        f"Indexing {len(files)} files..."
    )

    for p in tqdm(files):

        if file_exists(
                conn,
                p):
            continue

        insert_file(
            conn,
            p,
            p.name,
            p.suffix.lower(),
            p.stat().st_size
        )


def hash_files(conn):

    cur = conn.cursor()

    cur.execute("""
        SELECT
            source_path,
            size
        FROM files
        WHERE sha256 IS NULL
    """)

    rows = cur.fetchall()

    for row in tqdm(rows):

        path = Path(
            row["source_path"]
        )

        if not path.exists():
            continue

        try:
            ph = partial_hash(
                path
            )

            sha = full_hash(
                path
            )

            existing = find_by_sha(
                conn,
                sha
            )

            if (
                existing
                and
                existing["source_path"]
                != str(path)
            ):

                set_duplicate(
                    conn,
                    path,
                    existing["id"]
                )

                write_duplicate(
                    str(path),
                    existing[
                        "source_path"
                    ],
                    sha
                )

                continue

            update_hashes(
                conn,
                path,
                ph,
                sha
            )

        except Exception as e:
            write_failure(
                str(path),
                str(e)
            )


def enrich_metadata(conn):

    cur = conn.cursor()

    cur.execute("""
        SELECT source_path
        FROM files
        WHERE capture_date IS NULL
          AND status != 'duplicate'
    """)

    rows = cur.fetchall()

    for row in tqdm(rows):

        path = Path(
            row["source_path"]
        )

        if not path.exists():
            continue

        try:
            dt = get_capture_date(
                path
            )

            lat, lon, city, country = (
                get_gps(path)
            )

            category = classify(
                path
            )

            update_metadata(
                conn,
                path,
                dt.isoformat(),
                lat,
                lon,
                city,
                country,
                category
            )

        except Exception as e:
            write_failure(
                str(path),
                str(e)
            )


def detect_and_save_events(
        conn):

    rows = get_all_metadata(
        conn
    )

    items = []

    for r in rows:

        if not r["capture_date"]:
            continue

        items.append({
            "path":
                r["source_path"],
            "date":
                datetime.fromisoformat(
                    r["capture_date"]
                ),
            "city":
                r["city"]
        })

    events = detect_events(
        items
    )

    for item in items:

        day = item[
            "date"
        ].date()

        if day in events:
            set_event(
                conn,
                item["path"],
                events[
                    day
                ]["name"]
            )


def destination_folder(
        row):

    dt = datetime.fromisoformat(
        row["capture_date"]
    )

    category = row[
        "category"
    ]

    event = row[
        "event_name"
    ]

    city = row["city"]

    if row["status"] == "duplicate":
        return (
            DEST_DIR
            / "Duplicates"
        )

    if category == "screenshots":
        return (
            DEST_DIR
            / "Screenshots"
            / str(dt.year)
        )

    if category == "whatsapp":
        return (
            DEST_DIR
            / "WhatsApp"
            / str(dt.year)
        )

    if event:
        return (
            DEST_DIR
            / "Events"
            / event
        )

    month = (
        f"{dt.year}"
        f"-{dt.month:02d}"
    )

    if city:
        return (
            DEST_DIR
            / "Photos"
            / str(dt.year)
            / f"{month}_{city}"
        )

    return (
        DEST_DIR
        / "Photos"
        / str(dt.year)
        / month
    )


def move_files(conn):

    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM files
        WHERE status != 'moved'
    """)

    rows = cur.fetchall()

    for row in tqdm(rows):

        source = Path(
            row["source_path"]
        )

        if not source.exists():
            continue

        try:
            folder = (
                destination_folder(
                    row
                )
            )

            target = move_file(
                source,
                folder
            )

            update_destination(
                conn,
                source,
                target
            )

            write_move(
                str(source),
                str(target)
            )

            thumb = (
                create_thumbnail(
                    target
                )
            )

            if thumb:
                cur.execute("""
                    UPDATE files
                    SET thumbnail_path=?
                    WHERE source_path=?
                """,
                (
                    str(thumb),
                    str(source)
                ))

                conn.commit()

        except Exception as e:
            write_failure(
                str(source),
                str(e)
            )
            set_status(
                conn,
                source,
                "failed",
                str(e)
            )


def main():

    conn = (
        initialize_database()
    )

    files = scan_files()

    index_files(
        conn,
        files
    )

    hash_files(
        conn
    )

    enrich_metadata(
        conn
    )

    detect_and_save_events(
        conn
    )

    move_files(
        conn
    )

    print(
        "Organization complete."
    )


if __name__ == "__main__":
    main()