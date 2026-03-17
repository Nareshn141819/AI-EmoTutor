from fastapi import FastAPI, UploadFile, File
import whisper
import shutil
import requests
from emotion import detect_emotion
from tutor import tutor_mode, generate_response

app = FastAPI()

whisper_model = whisper.load_model("base")

MURF_API_KEY = "YOUR_MURF_API_KEY"


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

    # Speech to text
    result = whisper_model.transcribe(file_path)
    text = result["text"]

    # Emotion
    emotion = detect_emotion(text)

    # Tutor logic
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
        "audio": audio_file
    }
