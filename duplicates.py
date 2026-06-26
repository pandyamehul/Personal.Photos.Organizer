import hashlib

def partial_hash(path, size=65536):
    h = hashlib.md5()
    with open(path, "rb") as f:
        h.update(f.read(size))
    return h.hexdigest()


def full_hash(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()