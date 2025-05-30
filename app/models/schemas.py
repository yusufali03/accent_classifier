from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    status: str
    video_path: str | None = None
    audio_path: str | None = None
    accent: str | None = None
    confidence: float | None = None
    message: str | None = None