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

def speech_to_text(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=audio_file
            )
        print("📝 Transcribed Text:")
        print(transcript.text)
        
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

    # 🎤 SPEECH TO TEXT
    print("Step 2: Converting speech to text")
    steps.append("Step 2: Converting speech to text")

    text = speech_to_text(file_path)

    print("Recognized Text:", text)

    if not text or len(text) < 3:
        return {
            "steps": steps,
            "response": "I couldn't understand your voice. Please speak clearly.",
            "audio": None
        }

    # 😊 EMOTION
    print("Step 3: Emotion detected")
    steps.append("Step 3: Emotion detected")

    emotion = detect_emotion(text)

    # 🤖 GEMINI
    print("Step 4: Generating response")
    steps.append("Step 4: Generating response")

    mode = tutor_mode(emotion)
    tutor_text = generate_response(text, mode)

    print("Step 5: Response ready")
    steps.append("Step 5: Response ready")

    # 🔊 MURF
    print("Step 6: Generating voice")
    steps.append("Step 6: Generating voice")

    audio_file = murf_voice(tutor_text)

    print("Step 7: Done")
    steps.append("Step 7: Done")

    return {
        "steps": steps,
        "response": tutor_text,
        "audio": f"/audio/{audio_file}" if audio_file else None
    }
