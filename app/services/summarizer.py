# app/services/summarizer.py

from transformers import pipeline
from typing import List

# Cache the summarizer pipeline
_summarizer = None

def load_summarizer(model_name: str = "facebook/bart-large-cnn"):
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline("summarization", model=model_name)
    return _summarizer

def chunk_text(text: str, max_chars: int = 1000) -> List[str]:
    """
    Break text into chunks no longer than `max_chars` for models with input limits.
    Splits on sentence boundaries if possible.
    """
    import re

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chars:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def summarize_text(text: str, max_length: int = 60, min_length: int = 20) -> str:
    """
    Summarize long or short text by chunking if necessary.
    """
    if not text.strip():
        return "No transcript to summarize."

    summarizer = load_summarizer()
    chunks = chunk_text(text)

    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=max_length, min_length=min_length, do_sample=False)
            summaries.append(summary[0]["summary_text"].strip())
        except Exception as e:
            summaries.append(f"[Error summarizing chunk: {str(e)}]")

    return " ".join(summaries).strip()
