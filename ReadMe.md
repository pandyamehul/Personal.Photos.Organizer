# 📸 Local Photo Organizer (iPhone Backup Manager)

A local, offline photo management system for organizing large iPhone photo libraries (50k–100k+ files).

Features:

- 🧠 Duplicate detection (SHA256)
- 📅 Timeline view (like Google Photos)
- 🌍 Map view (GPS-based photo locations)
- 🧾 Event detection (trip / burst clustering)
- 📂 Auto categorization (Photos, WhatsApp, Screenshots)
- 🖼 Thumbnail-based gallery UI
- 🗄 SQLite-backed indexing (resume-safe)
- ⚡ Fully offline processing

---

## 🧰 Requirements

- Python 3.10+
- Windows 10/11 (tested target)
- ~5–10 GB free disk (thumbnails + DB + processing overhead)

---

## ⚡ Setup using `uv` (recommended)

Install uv if not installed:

```bash
pip install uv
```

## Create a virtual environment and install dependencies:

```bash
python -m venv venv
venv\Scripts\activate
uv add requirements.txt
```

## 🚀 Run Photo Organizer (CLI)

This processes and organizes your files:

```bash
python organizer.py
```

## What it does:

- scans all media files
- builds SQLite index
- detects duplicates
- extracts metadata (date + GPS)
- detects events (trips)
- moves files into structure
- generates thumbnails
- logs everything

## 📂 Output structure

After processing:

```
OrganizedPhotos/
│
├── Photos/
├── Events/
├── WhatsApp/
├── Screenshots/
├── Duplicates/
├── thumbnails/
├── logs/
└── photos.db
```

## 🧠 Run Web UI (Dashboard)

Start Flask server:

```bash
python app.py
```

Then open in browser:

```
http://localhost:5000
```
