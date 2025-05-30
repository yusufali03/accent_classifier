from transformers import pipeline
from app.config import ACCEPTED_ACCENT_CLASSES

# Cache the model to avoid reloading on every request
_model = None


def classify_accent(audio_path: str) -> dict:
    global _model
    if _model is None:
        _model = pipeline(
            "audio-classification",
            model="dima806/english_accents_classification"
        )

    result = _model(audio_path, top_k=1)[0]

    # Normalize the label to match our accepted classes
    label = result["label"]
    if "American" in label:
        label = "American"
    elif "British" in label or "England" in label:
        label = "British"
    elif "Australian" in label:
        label = "Australian"
    elif "Indian" in label:
        label = "Indian"
    elif "Canadian" in label:
        label = "Canadian"

    return {
        "accent": label,
        "confidence": round(result["score"] * 100, 2)
    }

# let's append here l have some mistaken for mentioning limited accents let's modify it for all that models accent classifiyings if possible