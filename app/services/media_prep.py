# app/services/media_prep.py

import re
from app.services.downloader import download_media      # your downloader
from app.services.extractor import extract_audio        # your extractor
from app.config import DOWNLOAD_DIR, AUDIO_DIR

def prepare_audio_from_url(url: str) -> str:
    """
    1. Downloads the media (YouTube, Loom or MP4) into DOWNLOAD_DIR.
    2. If it’s already a .wav (YouTube download/extraction), returns it.
    3. Otherwise, calls extract_audio() to convert it to a WAV in AUDIO_DIR.
    """
    # 1️⃣ Download to DOWNLOAD_DIR
    media_path = download_media(url, DOWNLOAD_DIR)

    # 2️⃣ If it’s already WAV, we’re done
    if media_path.lower().endswith(".wav"):
        return media_path

    # 3️⃣ Otherwise, extract to AUDIO_DIR
    audio_path = extract_audio(media_path)
    return audio_path
