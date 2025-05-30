<<<<<<< HEAD
# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
=======
# Accent Analyzer

A web application that classifies English accents from video input. Users can paste a public video URL (YouTube, Loom, or direct MP4) or upload a local video file. The backend (FastAPI) extracts audio, transcribes speech, classifies the speaker’s English accent (e.g., American, British, Australian, Indian, Canadian), and returns a short summary with a confidence score. The frontend (React) provides a simple UI to interact with the API.

---

## Live Demo

* **Frontend:** [https://your-frontend.vercel.app](https://your-frontend.vercel.app)

---

## Features

* **Video Input:** Accepts YouTube, Loom, direct MP4 URLs, or local file uploads
* **Audio Extraction:** Converts video to 16 kHz mono WAV using FFmpeg
* **Speech Transcription:** Uses OpenAI Whisper for robust English transcription
* **Accent Classification:** Classifies among English accents with a confidence score using a pre-trained model
* **Summarization:** Provides a concise summary of the spoken content
* **Progress Indicator:** Frontend shows dynamic progress bar during processing

---

## Architecture

```
[React Frontend] ←→ [FastAPI Backend]
                          │
                     services:
                       • downloader
                       • extractor (FFmpeg)
                       • asr (Whisper)
                       • classifier (HF model)
                       • summarizer (HF BART)
```

---

## Technologies

* **Frontend:** React, Vite, JavaScript, CSS
* **Backend:** Python, FastAPI, Uvicorn, FFmpeg
* **ML Libraries:** OpenAI Whisper, Hugging Face Transformers, SpeechBrain (optional)
* **Deployment:** Vercel (frontend), Render/PythonAnywhere (backend, HTTPS)

---

## Repository Structure

```
D:/AI_Project/
├── app/                   # FastAPI backend
│   ├── api/               # Route definitions
│   ├── services/          # Core functions (download, extract, classify, summarize)
│   ├── tests/             # Unit tests (pytest)
│   ├── models/            # Local caches of ML models
│   ├── main.py            # FastAPI entrypoint
│   ├── config.py          # Environment variables and settings
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── README.md
└── .gitignore
```

---

## Getting Started

### Prerequisites

* **Backend:** Python 3.8+, FFmpeg
* **Frontend:** Node.js 16+ and npm

### Environment Variables

Create a `.env` file in each root:

**Backend (****`app/.env`****):**

```
DOWNLOAD_DIR=./downloads
AUDIO_DIR=./audio_files
API_KEY=...          # (if any)
```

**Frontend (****`frontend/.env`****):**

```
VITE_API=https://your-backend.example.com/api
```

### Local Development

1. **Clone Repos:**

   ```bash
   git clone https://github.com/yourusername/accent-analyzer-backend.git
   git clone https://github.com/yourusername/accent-analyzer-frontend.git
   ```

2. **Run Backend:**

   ```bash
   cd accent-analyzer-backend/app
   python -m venv venv && source venv/bin/activate  # or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Run Frontend:**

   ```bash
   cd accent-analyzer-frontend
   npm install
   npm run dev
   ```

4. Open **[http://localhost:3000](http://localhost:3000)** to interact with the frontend.

---

## API Documentation

### POST `/api/analyze`

* **Description:** Analyze a video URL for English accent classification and summary.
* **Request:** `application/json`

  ```json
  { "url": "https://youtu.be/abcdef" }
  ```
* **Response:**

  ```json
  {
    "accent": "British",
    "confidence": 92.45,
    "summary": "Short summary of the speech."
  }
  ```

### POST `/api/analyze-upload`

* **Description:** Upload a local video file for analysis.
* **Request:** `multipart/form-data` with field `file`
* **Response:** Same schema as `/api/analyze`.

---

## Running Tests

From the **backend** directory:

```bash
pytest
```

---

## Evaluation Criteria

* **Functional Script:** Run accent classification on a variety of video inputs
* **Logical Approach:** Uses robust ASR and ML methods for transcription, classification, and summarization
* **Setup Clarity:** Clear `README.md` with step-by-step instructions
* **Accent Handling:** Focused on English accents only
* **Bonus:** Confidence scoring and UX polish with progress indicator

---

## Deployment

* **Frontend:** [https://your-frontend.vercel.app](https://your-frontend.vercel.app)
* **Backend:** [https://your-backend.example.com/api](https://your-backend.example.com/api)

---

## License

This project is licensed under the MIT License. Feel free to clone and modify for educational purposes.

>>>>>>> 3dfc915a3b85c76a5a8689f8f48f5e0b299e7635
