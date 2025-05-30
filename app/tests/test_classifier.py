from app.services.classifier import classify_accent

def test_classify_accent_on_sample():
    test_audio = "tests/sample.wav"  # should be short/valid
    result = classify_accent(test_audio)
    assert "accent" in result
    assert "confidence" in result
    assert isinstance(result["accent"], str)
    assert isinstance(result["confidence"], float)
