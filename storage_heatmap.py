from database import get_connection
from collections import defaultdict


def compute_heatmap():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT capture_date, size
        FROM files
        WHERE capture_date IS NOT NULL
    """)

    rows = cur.fetchall()

    heatmap = defaultdict(int)

    for r in rows:
        if not r["capture_date"]:
            continue

        year = r["capture_date"][:4]

        heatmap[year] += r["size"] or 0

    return {
        k: round(v / (1024**3), 2)
        for k, v in heatmap.items()
    }