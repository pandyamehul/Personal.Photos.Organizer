# app.py

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    abort
)

from pathlib import Path
from collections import defaultdict
from datetime import datetime

from gallery import *

app = Flask(__name__)


@app.route("/")
def home():
    stats = get_stats()
    return render_template(
        "index.html",
        stats=stats
    )


@app.route("/gallery")
def gallery():

    category = request.args.get(
        "category"
    )

    page = int(
        request.args.get(
            "page",
            0
        )
    )

    images = get_gallery(
        category,
        page
    )

    return render_template(
        "gallery.html",
        images=images,
        category=category,
        page=page
    )


@app.route("/timeline")
def timeline():

    rows = get_timeline()

    grouped = defaultdict(list)

    for r in rows:

        dt = r["capture_date"]

        if not dt:
            continue

        day = (
            datetime
            .fromisoformat(dt)
            .strftime(
                "%Y-%m-%d"
            )
        )

        grouped[day].append(r)

    return render_template(
        "timeline.html",
        data=grouped
    )


@app.route("/duplicates")
def duplicates():

    rows = get_duplicates()

    return render_template(
        "duplicates.html",
        rows=rows
    )


@app.route("/events")
def events():

    rows = get_events()

    return render_template(
        "events.html",
        rows=rows
    )


@app.route("/map")
def map_view():

    rows = get_map_points()

    return render_template(
        "map.html",
        points=rows
    )


@app.route("/image")
def image():

    path = request.args.get(
        "path"
    )

    p = Path(path)

    if not p.exists():
        abort(404)

    return send_file(p)


@app.route("/thumbnail")
def thumbnail():

    path = request.args.get(
        "path"
    )

    p = Path(path)

    if not p.exists():
        abort(404)

    return send_file(p)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )