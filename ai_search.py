import torch
import clip
from PIL import Image
import numpy as np
import pickle
from database import get_connection
from pathlib import Path

MODEL, PREPROCESS = clip.load("ViT-B/32")


EMBED_FILE = "image_embeddings.pkl"


def build_embeddings():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT source_path
        FROM files
        WHERE media_type='photo'
    """)

    rows = cur.fetchall()

    embeddings = []

    for r in rows:
        path = Path(r["source_path"])

        try:
            image = PREPROCESS(Image.open(path)).unsqueeze(0)

            with torch.no_grad():
                emb = MODEL.encode_image(image).cpu().numpy()

            embeddings.append({
                "path": str(path),
                "embedding": emb
            })

        except:
            continue

    with open(EMBED_FILE, "wb") as f:
        pickle.dump(embeddings, f)


def search(query, top_k=20):
    import pickle

    with open(EMBED_FILE, "rb") as f:
        data = pickle.load(f)

    text = clip.tokenize([query])

    with torch.no_grad():
        text_emb = MODEL.encode_text(text).numpy()

    results = []

    for d in data:
        sim = np.dot(d["embedding"], text_emb.T)[0][0]
        results.append((sim, d["path"]))

    results.sort(reverse=True)

    return results[:top_k]