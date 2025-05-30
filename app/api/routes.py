# from fastapi import APIRouter, HTTPException
# from app.services.downloader import download_media
# from app.services.extractor import extract_audio
# from app.services.classifier import classify_accent
# from app.models.schemas import AnalyzeRequest, AnalyzeResponse
# import tempfile
# import shutil
# import os
#
# router = APIRouter()
#
#
# @router.post("/analyze", response_model=AnalyzeResponse)
# async def analyze_video(request: AnalyzeRequest):
#     try:
#         # Create a temporary directory for this request
#         with tempfile.TemporaryDirectory() as temp_dir:
#             print(f"Starting download for: {request.url}")
#
#             # Download the video
#             video_path = download_media(request.url, temp_dir)
#
#             # Extract audio if needed
#             if video_path.endswith(".wav"):
#                 audio_path = video_path
#             else:
#                 print(f"Extracting audio from: {video_path}")
#                 audio_path = extract_audio(video_path)
#
#             print(f"Audio ready at: {audio_path}")
#
#             # Classify accent
#             accent_result = classify_accent(audio_path)
#
#             return {
#                 "status": "success",
#                 "video_path": video_path,
#                 "audio_path": audio_path,
#                 "accent": accent_result["accent"],
#                 "confidence": accent_result["confidence"],
#                 "message": "Analysis complete"
#             }
#
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
#

# app/api/routes.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.asr import transcribe_audio
from fastapi import UploadFile, File
import shutil

from app.config import DOWNLOAD_DIR, AUDIO_DIR
from app.services.downloader import download_media
from app.services.extractor import extract_audio
from app.services.classifier import classify_accent
from app.services.summarizer import summarize_text

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    accent: str
    confidence: float
    summary: str

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_video(request: AnalyzeRequest):
    try:
        # Ensure directories exist
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(AUDIO_DIR, exist_ok=True)

        # 1. Download media into DOWNLOAD_DIR
        media_path = download_media(request.url, DOWNLOAD_DIR)
        print(f"Downloaded media to: {media_path}")

        # 2. Extract audio if needed
        if media_path.lower().endswith(".wav"):
            audio_path = media_path
        else:
            print(f"Extracting audio from: {media_path}")
            audio_path = extract_audio(media_path)
        print(f"Audio ready at: {audio_path}")

        # 3. Classify accent
        accent_result = classify_accent(audio_path)

        # 4. Summarize transcript (internal ASR not returned)
        # We re-transcribe only for summarization, not returned fully

        transcript, _ = transcribe_audio(audio_path)
        summary = summarize_text(transcript)

        return AnalyzeResponse(
            accent=accent_result["accent"],
            confidence=accent_result["confidence"],
            summary=summary,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze-upload", response_model=AnalyzeResponse)
async def analyze_uploaded_video(file: UploadFile = File(...)):
    try:
        # Ensure directories exist
        os.makedirs(DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(AUDIO_DIR, exist_ok=True)

        # Save the uploaded file to the downloads directory
        file_path = os.path.join(DOWNLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        print(f"Saved uploaded file to: {file_path}")

        # Extract audio if needed
        if file_path.lower().endswith(".wav"):
            audio_path = file_path
        else:
            print(f"Extracting audio from: {file_path}")
            audio_path = extract_audio(file_path)
        print(f"Audio ready at: {audio_path}")

        # Classify accent
        accent_result = classify_accent(audio_path)

        # Transcribe + Summarize
        transcript, _ = transcribe_audio(audio_path)
        summary = summarize_text(transcript)

        return AnalyzeResponse(
            accent=accent_result["accent"],
            confidence=accent_result["confidence"],
            summary=summary,
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))