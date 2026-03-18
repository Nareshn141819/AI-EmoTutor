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
import os

load_dotenv()

# load lightweight model
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def speech_to_text(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )
        return transcript.text.strip()
    except Exception as e:
        print("STT ERROR:", e)
        return ""


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

    response = requests.post(url, json=payload, headers=headers, timeout=10)

    if response.status_code != 200:
        return None

    data = response.json()
    audio_url = data["audioFile"]

    audio_data = requests.get(audio_url).content

    file_path = "output.mp3"

    with open(file_path, "wb") as f:
        f.write(audio_data)

    return file_path


from fastapi.responses import JSONResponse

@app.post("/analyze/")
async def analyze(file: UploadFile = File(...)):

    steps = []

    print("Step 1: File received")
    steps.append("Step 1: File received")

    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🎤 AUDIO → TEXT
    print("Step 2: Converting audio to text...")
    steps.append("Step 2: Converting audio to text...")

    try:
        result = whisper_model.transcribe(file_path)
        text = result["text"]
    except Exception as e:
        print("Whisper Error:", e)
        text = "Could not understand audio"

    print("Recognized Text:", text)

    # 😊 Emotion
    print("Step 3: Emotion detected!")
    steps.append("Step 3: Emotion detected!")

    emotion = detect_emotion(text)

    # 🤖 Gemini
    print("Step 4: Response starting")
    steps.append("Step 4: Response starting")

    mode = tutor_mode(emotion)
    tutor_text = generate_response(text, mode)

    print("Step 5: Response done")
    steps.append("Step 5: Response done")

    # 🔊 Murf
    print("Step 6: AI Starting speech generating...")
    steps.append("Step 6: AI Starting speech generating...")

    audio_file = murf_voice(tutor_text)

    print("Step 7: Speech Done...")
    steps.append("Step 7: Speech Done...")

    print("Recognized Text:", text)

    return JSONResponse({
        "response": tutor_text,
        "audio": f"/audio/{audio_file}" if audio_file else None
    })
