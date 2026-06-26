# gallery.py

from database import get_connection


def get_stats():
    conn = get_connection()
    cur = conn.cursor()

    stats = {}

    cur.execute("""
        SELECT COUNT(*)
        FROM files
    """)
    stats["total"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE status='duplicate'
    """)
    stats["duplicates"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE category='screenshots'
    """)
    stats["screenshots"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE category='whatsapp'
    """)
    stats["whatsapp"] = cur.fetchone()[0]

    cur.execute("""
        SELECT COUNT(*)
        FROM files
        WHERE event_name IS NOT NULL
    """)
    stats["events"] = cur.fetchone()[0]

    cur.execute("""
        SELECT ROUND(
            SUM(size)/1024.0/1024.0/1024.0,
            2
        )
        FROM files
    """)
    stats["size_gb"] = cur.fetchone()[0] or 0

    conn.close()
    return stats


def get_gallery(
        category=None,
        page=0,
        page_size=200):

    conn = get_connection()
    cur = conn.cursor()

    offset = page * page_size

    sql = """
        SELECT
            current_path,
            thumbnail_path,
            capture_date,
            category,
            city
        FROM files
        WHERE status='moved'
    """

    params = []

    if category:
        sql += " AND category=? "
        params.append(category)

    sql += """
        ORDER BY capture_date DESC
        LIMIT ?
        OFFSET ?
    """

    params.extend([
        page_size,
        offset
    ])

    cur.execute(sql, params)
    rows = cur.fetchall()

    conn.close()
    return rows


def get_duplicates():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            source_path,
            duplicate_of,
            current_path
        FROM files
        WHERE status='duplicate'
    """)

    rows = cur.fetchall()

    conn.close()
    return rows


def get_events():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            event_name,
            COUNT(*) AS count,
            MIN(capture_date),
            MAX(capture_date)
        FROM files
        WHERE event_name IS NOT NULL
        GROUP BY event_name
        ORDER BY MIN(capture_date)
    """)

    rows = cur.fetchall()

    conn.close()
    return rows


def get_timeline():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            current_path,
            thumbnail_path,
            capture_date
        FROM files
        WHERE status='moved'
        ORDER BY capture_date DESC
    """)

    rows = cur.fetchall()

    conn.close()
    return rows


def get_map_points():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            latitude,
            longitude,
            city,
            current_path
        FROM files
        WHERE latitude IS NOT NULL
          AND longitude IS NOT NULL
          AND status='moved'
    """)

    rows = cur.fetchall()

    conn.close()
    return rows