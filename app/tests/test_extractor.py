import os
from app.services.extractor import extract_audio

def test_extract_audio():
    test_video = "tests/sample.mp4"  # small test video file
    audio_path = extract_audio(test_video)
    assert os.path.exists(audio_path)
    assert audio_path.endswith(".wav")
