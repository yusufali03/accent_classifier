from app.services.summarizer import summarize_text

def test_summarize_text():
    text = "This is a simple test sentence repeated. " * 10
    summary = summarize_text(text)
    assert isinstance(summary, str)
    assert len(summary) < len(text)
