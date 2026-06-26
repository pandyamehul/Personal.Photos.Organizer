import sqlite3
from config import DB_PATH, DEST_DIR


def get_connection():
    DEST_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            source_path TEXT UNIQUE NOT NULL,
            current_path TEXT,

            filename TEXT NOT NULL,
            extension TEXT,
            size INTEGER,

            partial_hash TEXT,
            sha256 TEXT,

            capture_date TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            modified_at TEXT,

            latitude REAL,
            longitude REAL,
            city TEXT,
            country TEXT,

            category TEXT,
            media_type TEXT,

            event_name TEXT,

            live_photo_group TEXT,

            status TEXT DEFAULT 'indexed',

            duplicate_of INTEGER,

            destination_path TEXT,

            thumbnail_path TEXT,

            error_message TEXT,

            FOREIGN KEY (duplicate_of)
                REFERENCES files(id)
        );

        CREATE INDEX IF NOT EXISTS idx_sha256
            ON files(sha256);

        CREATE INDEX IF NOT EXISTS idx_capture_date
            ON files(capture_date);

        CREATE INDEX IF NOT EXISTS idx_category
            ON files(category);

        CREATE INDEX IF NOT EXISTS idx_city
            ON files(city);

        CREATE INDEX IF NOT EXISTS idx_status
            ON files(status);

        CREATE INDEX IF NOT EXISTS idx_live_group
            ON files(live_photo_group);
        """
    )

    conn.commit()
    return conn

def file_exists(conn, source_path):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id
        FROM files
        WHERE source_path=?
        """,
        (str(source_path),),
    )

    return cur.fetchone()


def insert_file(
    conn,
    source_path,
    filename,
    extension,
    size,
):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO files
        (
            source_path,
            filename,
            extension,
            size
        )
        VALUES
        (?, ?, ?, ?)
        """,
        (
            str(source_path),
            filename,
            extension,
            size,
        ),
    )

    conn.commit()


def update_hashes(
    conn,
    source_path,
    partial,
    sha,
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE files
        SET partial_hash=?,
            sha256=?
        WHERE source_path=?
        """,
        (
            partial,
            sha,
            str(source_path),
        ),
    )

    conn.commit()
    
def update_metadata(
    conn,
    source_path,
    capture_date,
    lat,
    lon,
    city,
    country,
    category,
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE files
        SET
            capture_date=?,
            latitude=?,
            longitude=?,
            city=?,
            country=?,
            category=?
        WHERE source_path=?
        """,
        (
            capture_date,
            lat,
            lon,
            city,
            country,
            category,
            str(source_path),
        ),
    )

    conn.commit()

def set_duplicate(
    conn,
    source_path,
    duplicate_id,
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE files
        SET
            duplicate_of=?,
            status='duplicate'
        WHERE source_path=?
        """,
        (
            duplicate_id,
            str(source_path),
        ),
    )

    conn.commit()

def update_destination(
    conn,
    source_path,
    destination,
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE files
        SET
            destination_path=?,
            current_path=?,
            status='moved'
        WHERE source_path=?
        """,
        (
            str(destination),
            str(destination),
            str(source_path),
        ),
    )

    conn.commit()
    
def set_event(
    conn,
    source_path,
    event_name,
):
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE files
        SET
            event_name=?
        WHERE source_path=?
        """,
        (
            event_name,
            str(source_path),
        ),
    )

    conn.commit()

def get_unprocessed_files(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM files
        WHERE status IS NULL
           OR status='indexed'
           OR status='metadata'
    """)

    return cur.fetchall()

def find_by_sha(conn, sha):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, source_path
        FROM files
        WHERE sha256=?
    """, (sha,))

    return cur.fetchone()

def set_status(
        conn,
        source_path,
        status,
        error=None):

    cur = conn.cursor()

    cur.execute("""
        UPDATE files
        SET status=?,
            error_message=?
        WHERE source_path=?
    """,
    (
        status,
        error,
        str(source_path)
    ))

    conn.commit()

def get_all_metadata(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT
            source_path,
            capture_date,
            city
        FROM files
        WHERE capture_date IS NOT NULL
    """)

    return cur.fetchall()