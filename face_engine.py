import face_recognition
import numpy as np
from pathlib import Path
import pickle
from database import get_connection


ENCODINGS_FILE = "faces.pkl"


def extract_faces(image_path):
    image = face_recognition.load_image_file(image_path)
    locations = face_recognition.face_locations(image)

    encodings = face_recognition.face_encodings(image, locations)

    return encodings


def build_face_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT source_path
        FROM files
        WHERE media_type='photo'
    """)

    rows = cur.fetchall()

    all_encodings = []

    for r in rows:
        path = Path(r["source_path"])

        try:
            encs = extract_faces(path)

            for e in encs:
                all_encodings.append({
                    "path": str(path),
                    "encoding": e
                })

        except:
            continue

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(all_encodings, f)


def cluster_faces():
    import pickle
    from sklearn.cluster import DBSCAN

    with open(ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    encodings = [d["encoding"] for d in data]

    X = np.array(encodings)

    clustering = DBSCAN(
        eps=0.45,
        min_samples=3,
        metric="euclidean"
    ).fit(X)

    groups = {}

    for idx, label in enumerate(clustering.labels_):

        if label == -1:
            continue

        groups.setdefault(label, []).append(
            data[idx]["path"]
        )

    return groups