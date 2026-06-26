from ai_search import search as clip_search
from database import get_connection


def search_all(query):
    conn = get_connection()
    cur = conn.cursor()

    # 1. semantic search (AI)
    try:
        ai_results = clip_search(query, top_k=10)
    except:
        ai_results = []

    # 2. metadata search
    cur.execute("""
        SELECT source_path
        FROM files
        WHERE
            city LIKE ?
            OR event_name LIKE ?
            OR capture_date LIKE ?
        LIMIT 20
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))

    meta = [r["source_path"] for r in cur.fetchall()]

    # merge + dedupe
    seen = set()
    results = []

    for _, p in ai_results:
        if p not in seen:
            results.append(p)
            seen.add(p)

    for p in meta:
        if p not in seen:
            results.append(p)
            seen.add(p)

    return results