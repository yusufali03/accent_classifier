# app/services/asr.py

import whisper
from typing import Tuple

# Cache the Whisper model
_model = None

def load_asr_model(model_size: str = "small") -> whisper.Whisper:
    global _model
    if _model is None:
        _model = whisper.load_model(model_size)
    return _model

def transcribe_audio(audio_path: str) -> Tuple[str, float]:
    """
    Transcribe audio to text.
    Returns: (transcript, duration_seconds)
    """
    model = load_asr_model()
    result = model.transcribe(audio_path, verbose=False)
    # result["text"] is the full transcription
    # result["segments"] has per-segment info if you need it
    # result["duration"] gives audio length in seconds
    transcript = result["text"].strip()
    duration = result.get("duration", 0.0)
    return transcript, duration
