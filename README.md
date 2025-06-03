Accent Analyzer
A web application that classifies English accents from video input. Users can paste a public video URL (YouTube, Loom, or direct MP4) or upload a local video file. The backend (FastAPI) extracts audio, transcribes speech, classifies the speaker’s English accent (e.g., American, British, Australian, Indian, Canadian), and returns a short summary with a confidence score. The frontend (React + Vite) provides a simple UI to interact with the API.

Live Demo
Frontend: https://accent-classifier-68m6.vercel.app
Backend: (Deployed URL or placeholder; e.g., https://your-backend.example.com/api)

Table of Contents
Features

Architecture

Prerequisites

Repository Structure

Getting Started

Clone the Repository

Backend Setup (CPU-only)

Frontend Setup

Run Locally

API Documentation

POST /api/analyze

POST /api/analyze-upload

Optional: GPU Acceleration

Enable GPU on a Cloud VM

Install CUDA-compatible PyTorch & Whisper

Update Code to Use GPU

Configuration & Environment Variables

Troubleshooting & Notes

Deployment Suggestions

License & Acknowledgments

Features
Video Input: Accepts YouTube, Loom, direct MP4 URLs, or local file uploads

Audio Extraction: Converts video to 16 kHz mono WAV using FFmpeg

Speech Transcription: Uses OpenAI Whisper for robust English transcription

Accent Classification: Classifies among English accents with a confidence score using a pretrained model (dima806/english_accents_classification)

Summarization: Provides a concise summary of the spoken content using a distilBART model (sshleifer/distilbart-cnn-12-6)

Progress Indicator: Frontend shows a dynamic progress bar during processing

Architecture
css
Copy
Edit
[React Frontend] ←→ [FastAPI Backend]
                          │
                     services:
                       • downloader (yt-dlp / pytube)
                       • extractor (FFmpeg)
                       • asr (OpenAI Whisper)
                       • classifier (HF Wav2Vec2)
                       • summarizer (HF distilBART)
Prerequisites
Operating System:

Ubuntu 20.04/22.04 (recommended for deployment)

macOS or Windows (WSL2) for local development

Python: 3.10 – 3.11

Node.js: ≥ 16.x and npm ≥ 8.x

FFmpeg: must be installed and on your PATH

Git: to clone the repository

On Ubuntu:

bash
Copy
Edit
sudo apt update
sudo apt install -y ffmpeg git python3-venv
On macOS (with Homebrew):

bash
Copy
Edit
brew install ffmpeg git
Repository Structure
graphql
Copy
Edit
accent-analyzer/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py       # Route definitions
│   │   ├── services/           # Core logic: downloader, extractor, ASR, classifier, summarizer
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── config.py           # Environment variables and settings
│   │   └── requirements.txt    # Python dependencies
│   ├── venv/                   # Python virtual environment (created during setup)
│   └── README-backend.md       # Backend-specific instructions (this file covers both)
│
├── frontend/                   # React / Vite frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── README-frontend.md      # Frontend-specific instructions
│
├── .gitignore
└── README.md                   # Project overview (this file)
Getting Started
Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/accent-analyzer.git
cd accent-analyzer
Backend Setup (CPU-only)
Navigate to the backend directory and create a virtual environment:

bash
Copy
Edit
cd backend
python3 -m venv venv
source venv/bin/activate
Install dependencies:

bash
Copy
Edit
pip install --upgrade pip
pip install -r requirements.txt
This will install:

css
Copy
Edit
fastapi
uvicorn[standard]
torch
transformers
openai-whisper
yt-dlp
pytube
python-multipart
Install FFmpeg (if not already on your system):

bash
Copy
Edit
# Ubuntu / Debian
sudo apt install -y ffmpeg

# macOS (Homebrew)
brew install ffmpeg
Set up a cache directory for Hugging Face models to avoid filling your home partition:

bash
Copy
Edit
export HF_HOME="$PWD/hf_cache"
mkdir -p hf_cache
You can add that line to your ~/.bashrc or ~/.zshrc so it persists:

bash
Copy
Edit
echo 'export HF_HOME="$PWD/hf_cache"' >> ~/.bashrc
(Optional) Enable swap if you have limited RAM (< 8 GB) and want to avoid OOM when loading large models:

bash
Copy
Edit
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
Frontend Setup
Navigate to the frontend directory:

bash
Copy
Edit
cd ../frontend
Install Node dependencies:

bash
Copy
Edit
npm install
Configure the API base URL
In frontend/src/config.js, adjust:

js
Copy
Edit
export const API_BASE = "http://localhost:8000";
When you deploy, change this to:

js
Copy
Edit
export const API_BASE = "https://your-backend.example.com/api";
Run Locally
Start the Backend
In one terminal (inside backend/, with the virtual environment activated):

bash
Copy
Edit
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
The --reload flag is for development; remove it in production.

The API will listen at http://localhost:8000.

You can view the interactive docs at http://localhost:8000/docs.

Start the Frontend
In a separate terminal (inside frontend/):

bash
Copy
Edit
npm run dev
Vite will serve the React app at http://localhost:3000.

Use the web UI to submit a YouTube or MP4 URL, or upload a file.

API Documentation
POST /api/analyze
Description: Analyze a video URL for accent classification and summary.

Request Header:
Content-Type: application/json

Request Body:

json
Copy
Edit
{
  "url": "https://www.youtube.com/watch?v=abcdef12345"
}
Response Body:

json
Copy
Edit
{
  "accent": "Indian",
  "confidence": 0.92,
  "summary": "Speaker introduces themselves and discusses their …"
}
Error Codes:

400 Bad Request if the "url" field is missing or invalid.

500 Internal Server Error if downloading or processing fails.

POST /api/analyze-upload
Description: Upload a local video file for analysis.

Request Header:
Content-Type: multipart/form-data

Request Body:

Field name: file

Value: <binary video/mp4> or other supported formats

Response Body: (Same as /api/analyze.)

Optional: GPU Acceleration
If you need faster inference, you can spin up a GPU-enabled VM (e.g., on GCP, AWS, or your local workstation with an NVIDIA GPU) and run Whisper + Hugging Face pipelines on the GPU instead of CPU.

Enable GPU on a Cloud VM (GCP Example)
Stop your existing VM (Compute Engine → VM instances → “⋮” → Stop).

Edit the VM → under “Machine configuration” click Add GPU → select 1 × NVIDIA T4.

Save and Start the VM.

SSH into the VM once it’s running.

Install CUDA-compatible PyTorch & Whisper
bash
Copy
Edit
# Example for Ubuntu 22.04
sudo apt update
sudo apt install -y build-essential dkms nvidia-driver-525 nvidia-cuda-toolkit
sudo reboot
After reboot:

bash
Copy
Edit
# Verify GPU is visible
nvidia-smi

# In the backend virtual environment:
cd ~/accent-analyzer/backend
source venv/bin/activate
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install --upgrade openai-whisper transformers
Update Code to Use GPU
app/services/asr.py:

python
Copy
Edit
import whisper, torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
whisper_model = whisper.load_model("tiny").to(DEVICE)

def transcribe_audio(audio_path: str):
    result = whisper_model.transcribe(audio_path, device=DEVICE)
    return result["text"], result
app/services/classifier.py:

python
Copy
Edit
from transformers import pipeline
import torch

DEVICE_IDX = 0 if torch.cuda.is_available() else -1
accent_classifier = pipeline(
    "audio-classification",
    model="dima806/english_accents_classification",
    device=DEVICE_IDX
)

def classify_accent(audio_path: str):
    preds = accent_classifier(audio_path)
    return {"accent": preds[0]["label"], "confidence": float(preds[0]["score"])}
app/services/summarizer.py:

python
Copy
Edit
from transformers import pipeline
import torch

SUMMARIZER_DEVICE = 0 if torch.cuda.is_available() else -1
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=SUMMARIZER_DEVICE
)

def summarize_text(text: str) -> str:
    outputs = summarizer(text, max_length=60, min_length=20)
    return outputs[0]["summary_text"]
Restart the backend service (if using systemd) or rerun Uvicorn. Inference will now run on the GPU, significantly reducing processing time (e.g., ~10–20 s per 1 min clip).

Configuration & Environment Variables
HF_HOME (or TRANSFORMERS_CACHE): Path to cache Hugging Face models.

bash
Copy
Edit
export HF_HOME="/path/to/accent-analyzer/backend/hf_cache"
Ensure that directory has sufficient disk space (≥ 5 GB).

API_BASE (frontend): In frontend/src/config.js, set:

js
Copy
Edit
export const API_BASE = "http://localhost:8000";
For production, change to:

js
Copy
Edit
export const API_BASE = "https://your-production-domain.com/api";
FFMPEG_PATH / FFPROBE_PATH: If FFmpeg is not on $PATH, set:

bash
Copy
Edit
export FFMPEG_PATH="/usr/bin/ffmpeg"
export FFPROBE_PATH="/usr/bin/ffprobe"
Troubleshooting & Notes
“No space left on device”

Ensure you’re downloading and caching to a disk with sufficient free space.

Use HF_HOME to redirect Hugging Face downloads to a larger disk.

For large models (BART-large-CNN ~1.6 GB), use the smaller sshleifer/distilbart-cnn-12-6 to reduce cache size.

“ffmpeg not found”

Install FFmpeg (sudo apt install ffmpeg or brew install ffmpeg).

If running under systemd, ensure /usr/bin is in the service’s PATH.

“module 'whisper' has no attribute 'load_model'”

Uninstall any incorrect whisper package (pip uninstall whisper).

Install OpenAI’s Whisper: pip install openai-whisper.

“ERROR: unable to download video data: HTTP Error 403: Forbidden”

Update download_youtube() in app/services/downloader.py:

python
Copy
Edit
ydl_opts = {
    ...,
    "nocheckcertificate": True,
    "geo_bypass": True,
    "ffmpeg_location": "/usr/bin/ffmpeg",
    "ffprobe_location": "/usr/bin/ffprobe",
    ...
}
Optionally use a fallback to pytube if yt-dlp still fails.

“Killed by OOM” on CPU-only VMs

Increase swap (sudo fallocate -l 4G /swapfile …).

Use smaller models: Whisper “tiny”, summarizer sshleifer/distilbart-cnn-12-6.

Or upgrade to a machine with ≥ 16 GB RAM (e.g., n1-standard-8 on GCP).

SSH access lost after resizing or metadata changes

Re-add your SSH key to instance metadata with the format:

ruby
Copy
Edit
<linux-username>:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC… comment
If OS-Login is enabled, either disable it on that VM or add your key to your OS-Login profile (IAM → OS-Login).

Deployment Suggestions
Server Setup (Ubuntu 22.04, CPU or GPU)

SSH into your server, clone the repo, set up venv, install dependencies, and configure HF_HOME.

Install ffmpeg and (if GPU) nvidia-driver & cuda.

Create a systemd service at /etc/systemd/system/accent-api.service:

ini
Copy
Edit
[Unit]
Description=Gunicorn instance to serve Accent Analyzer FastAPI
After=network.target

[Service]
User=your_user
Group=www-data
WorkingDirectory=/path/to/accent-analyzer/backend
Environment="PATH=/path/to/accent-analyzer/backend/venv/bin:/usr/bin"
Environment="HF_HOME=/path/to/accent-analyzer/backend/hf_cache"
ExecStart=/path/to/accent-analyzer/backend/venv/bin/gunicorn \
  -k uvicorn.workers.UvicornWorker \
  app.main:app \
  --bind 127.0.0.1:8000 \
  --workers 2 \
  --timeout 3600

[Install]
WantedBy=multi-user.target
Reload and start:

bash
Copy
Edit
sudo systemctl daemon-reload
sudo systemctl enable accent-api
sudo systemctl start accent-api
Nginx Reverse Proxy (HTTPS)

Install Nginx: sudo apt install -y nginx.

Configure /etc/nginx/sites-available/accent.example.com:

nginx
Copy
Edit
server {
    listen 80;
    server_name accent.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name accent.example.com;

    ssl_certificate     /etc/letsencrypt/live/accent.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/accent.example.com/privkey.pem;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers on;

    proxy_connect_timeout 3600s;
    proxy_send_timeout    3600s;
    proxy_read_timeout    3600s;
    send_timeout          3600s;

    location / {
        proxy_pass         http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_set_header   Upgrade $http_upgrade;
        proxy_set_header   Connection "upgrade";
    }
}
Enable and reload Nginx:

bash
Copy
Edit
sudo ln -s /etc/nginx/sites-available/accent.example.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
Frontend Deployment

Build the React app:

bash
Copy
Edit
cd frontend
npm run build
Deploy the contents of frontend/dist/ to any static hosting (e.g., Vercel, Netlify).

Ensure the API_BASE in your build points to your backend’s HTTPS URL.

Scaling & Background Tasks

For higher traffic or very long videos, consider offloading inference to a queue (Celery + Redis).

Enqueue jobs on /api/analyze, immediately return a job ID, and provide a /api/status/{job_id} route to fetch results once complete.

License & Acknowledgments
License: MIT License

Whisper by OpenAI: https://github.com/openai/whisper

Hugging Face Transformers: https://github.com/huggingface/transformers

dima806/english_accents_classification model: https://huggingface.co/dima806/english_accents_classification

sshleifer/distilbart-cnn-12-6 summarizer: https://huggingface.co/sshleifer/distilbart-cnn-12-6
