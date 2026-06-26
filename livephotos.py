# livephotos.py

from collections import defaultdict


def build_live_photo_groups(files):
    groups = defaultdict(list)

    for p in files:
        stem = p.stem.upper()

        if stem.startswith("IMG_"):
            groups[stem].append(p)

    return groups