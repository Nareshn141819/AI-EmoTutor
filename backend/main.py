from fastapi import FastAPI, UploadFile, File
import shutil
import requests
import os
from emotion import detect_emotion
from tutor import tutor_mode, generate_response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve audio files
app.mount("/audio", StaticFiles(directory="."), name="audio")

# ✅ API Keys from environment
MURF_API_KEY = os.getenv("MURF_API_KEY")


# 🔊 Murf Voice
def murf_voice(text):
    url = "https://api.murf.ai/v1/speech/generate"

    headers = {
        "api-key": MURF_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voiceId": "en-US-natalie",
        "format": "MP3"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()
    audio_url = data["audioFile"]

    audio_data = requests.get(audio_url).content

    file_path = "output.mp3"

    with open(file_path, "wb") as f:
        f.write(audio_data)

    return file_path


@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ❌ Removed Whisper (heavy)
    # ✅ TEMP: fake transcription (until you use API)
    text = "User uploaded audio"  

    # Emotion
    emotion = detect_emotion(text)

    # Mode
    mode = tutor_mode(emotion)

    # Gemini response
    tutor_text = generate_response(text, mode)

    # Murf voice
    audio_file = murf_voice(tutor_text)

    return {
        "text": text,
        "emotion": emotion,
        "mode": mode,
        "response": tutor_text,
        "audio": f"/audio/{audio_file}"
    }
