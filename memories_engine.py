from database import get_connection
from collections import defaultdict
from datetime import datetime, timedelta


def build_memories():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            source_path,
            capture_date,
            city,
            event_name
        FROM files
        WHERE capture_date IS NOT NULL
    """)

    rows = cur.fetchall()

    memories = defaultdict(list)

    for r in rows:
        dt = datetime.fromisoformat(r["capture_date"])

        # KEY IDEA 1: event-based memory
        if r["event_name"]:
            key = f"event:{r['event_name']}"
        else:
            # KEY IDEA 2: city + month grouping
            key = f"{r['city']}:{dt.year}-{dt.month:02d}"

        memories[key].append({
            "path": r["source_path"],
            "date": dt
        })

    return memories


def get_top_memories(limit=20):
    memories = build_memories()

    scored = []

    for k, items in memories.items():
        if len(items) < 5:
            continue

        items.sort(key=lambda x: x["date"])

        duration = (items[-1]["date"] - items[0]["date"]).days + 1

        score = len(items) * 2 + duration

        scored.append((score, k, items))

    scored.sort(reverse=True)

    return scored[:limit]