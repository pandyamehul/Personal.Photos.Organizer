# events.py

from collections import defaultdict
from datetime import timedelta
from config import EVENT_MIN_PHOTOS
from config import EVENT_MAX_GAP_HOURS


def detect_events(photo_metadata):
    """
    photo_metadata:
        [
            {
                path,
                date,
                city
            }
        ]
    """

    events = {}

    by_day = defaultdict(list)

    for item in photo_metadata:
        by_day[item["date"].date()].append(
            item
        )

    #
    # big days
    #

    for day, items in by_day.items():
        if len(items) >= EVENT_MIN_PHOTOS:
            city = (
                items[0]["city"]
                or "Event"
            )

            events[day] = {
                "name":
                    f"{day}_{city}",
                "count":
                    len(items),
            }

    #
    # cluster events
    #

    items = sorted(
        photo_metadata,
        key=lambda x: x["date"]
    )

    cluster = []

    for item in items:

        if not cluster:
            cluster.append(item)
            continue

        previous = cluster[-1]

        gap = (
            item["date"]
            - previous["date"]
        )

        if (
            gap
            <= timedelta(
                hours=EVENT_MAX_GAP_HOURS
            )
            and
            item["city"]
            == previous["city"]
        ):
            cluster.append(item)
        else:

            if (
                len(cluster)
                >= EVENT_MIN_PHOTOS
            ):
                d = cluster[0]["date"].date()
                c = (
                    cluster[0]["city"]
                    or "Event"
                )

                events[d] = {
                    "name":
                        f"{d}_{c}",
                    "count":
                        len(cluster),
                    "city": c,
                    "start":
                        cluster[0]["date"],
                    "end":
                        cluster[-1]["date"]
                }

            cluster = [item]

    return events