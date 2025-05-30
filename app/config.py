import os

# Base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Download directories
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
AUDIO_DIR = os.path.join(BASE_DIR, "audio_files")

# Create directories if they don't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Model configuration
ACCEPTED_URL_TYPES = ["youtube", "loom", "direct_mp4"]
ACCEPTED_AUDIO_FORMATS = ["wav", "mp3"]
ACCEPTED_ACCENT_CLASSES = ["American", "British", "Australian", "Indian", "Canadian"]