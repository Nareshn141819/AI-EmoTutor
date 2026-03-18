from fastapi import FastAPI, UploadFile, File
import shutil
import requests
import os
from emotion import detect_emotion
from tutor import tutor_mode, generate_response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import whisper
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 🎤 SPEECH TO TEXT
# =========================
def transcribe_audio(file_path):
    try:
        with open(file_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=f
            )
        print("📝 TEXT:", result.text)
        return result.text
    except Exception as e:
        print("❌ Transcription ERROR:", e)
        return "Could not understand audio"


# ✅ Serve audio files
app.mount("/audio", StaticFiles(directory="."), name="audio")



# ✅ API Keys from environment
MURF_API_KEY = os.getenv("MURF_API_KEY")


# =========================
# 🔊 MURF VOICE
# =========================
def murf_voice(text):
    if not MURF_API_KEY:
        return None

    try:
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

        res = requests.post(url, json=payload, headers=headers)

        if res.status_code != 200:
            print("❌ Murf Error:", res.text)
            return None

        audio_url = res.json()["audioFile"]
        audio_data = requests.get(audio_url).content

        file_path = "output.mp3"

        with open(file_path, "wb") as f:
            f.write(audio_data)

        return file_path

    except Exception as e:
        print("❌ Murf Exception:", e)
        return None





from fastapi.responses import JSONResponse

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    steps = []

    # Step 1
    print("Step 1: File received")
    steps.append("Step 1: File received")

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Step 2
    print("Step 2: Converting speech to text")
    steps.append("Step 2: Converting speech to text")

    text = transcribe_audio(file_path)

    # Step 3
    print("Step 3: Detecting emotion")
    steps.append("Step 3: Detecting emotion")

    emotion = detect_emotion(file_path)

    # Step 4
    print("Step 4: Generating AI response")
    steps.append("Step 4: Generating AI response")

    response_text = generate_response(text, emotion)

    # Step 5
    print("Step 5: Generating voice")
    steps.append("Step 5: Generating voice")

    audio_file = murf_voice(response_text)

    # Step 6
    print("Step 6: Done")
    steps.append("Step 6: Done")

    return JSONResponse({
        "steps": steps,
        "text": text,
        "emotion": emotion,
        "response": response_text,
        "audio": f"/{audio_file}" if audio_file else None
    })
