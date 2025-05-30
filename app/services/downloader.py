import os
import re
import yt_dlp
import requests
from app.config import DOWNLOAD_DIR

# Regular expressions to identify URL types
YOUTUBE_REGEX = r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|v/))([\w-]{11})"
LOOM_REGEX = r"loom\.com/(?:share|embed)/(\w+)"
MP4_REGEX = r"https?://.*\.(?:mp4|MP4)(?:[?&].*)?$"


def download_youtube(url: str, download_dir: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'verbose': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        audio_path = os.path.splitext(filename)[0] + ".wav"
    return audio_path


def download_direct_mp4(url: str, download_dir: str) -> str:
    local_filename = os.path.join(download_dir, os.path.basename(url.split('?')[0]))
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename


def download_loom(url: str, download_dir: str) -> str:
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(download_dir, '%(id)s.%(ext)s'),
        'verbose': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_media(url: str, download_dir: str = DOWNLOAD_DIR) -> str:
    os.makedirs(download_dir, exist_ok=True)

    if re.search(YOUTUBE_REGEX, url):
        print("Detected YouTube URL")
        return download_youtube(url, download_dir)
    elif re.search(LOOM_REGEX, url):
        print("Detected Loom URL")
        return download_loom(url, download_dir)
    elif re.search(MP4_REGEX, url):
        print("Detected direct MP4 URL")
        return download_direct_mp4(url, download_dir)
    else:
        raise ValueError("Unsupported URL format.")