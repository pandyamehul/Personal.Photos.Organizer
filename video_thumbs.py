import subprocess
from pathlib import Path


def generate_video_thumbnail(video_path, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-ss",
        "00:00:02",
        "-vframes",
        "1",
        str(output_path)
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_path


def is_video(path):
    return path.suffix.lower() in {".mov", ".mp4", ".m4v"}