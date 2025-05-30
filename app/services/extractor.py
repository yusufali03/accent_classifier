import subprocess
import os
from app.config import AUDIO_DIR


def extract_audio(video_path: str) -> str:
    base_name = os.path.basename(video_path)
    audio_path = os.path.join(AUDIO_DIR, os.path.splitext(base_name)[0] + ".wav")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        audio_path
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)
        return audio_path
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg error: {e.stderr.decode()}") from e